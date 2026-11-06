"""Morning missed-story check (added 2026-11-05, rewritten 2026-11-06). Registered as "Watch Missed Story Check", daily 08:20.

Compares the episode that aired today (site repo news/episodes/D.json) with the SAME story list the writers were given
(collectors/build_top.py: wire from yesterday 06:00 through 04:00 today + the Perplexity scout, grouped into stories by
collectors/story_cluster.py). Each story is listed ONCE with its outlet count. Writes
C:\\Users\\lilli\\AI-Shared\\state\\news-missed\\D.md.

Matching (no AI, plain words): a story is COVERED if one of its links is an episode source, or if ONE episode segment holds
at least 45% of the story's core words (rare names and numbers weigh more), or holds two of its names plus two other core
words (names and key nouns together). Paraphrase can still fool it, so a flagged story is a lead, not a verdict.

Buzz: ONE short line, ONLY when a MUST AIR story (3+ outlets, or a safety word) is missing: top 3 by outlet count + how many
more. The full report file is always written. Wire items first seen after 04:00 are listed separately and never count.

Usage: run_missed_check.py [YYYY-MM-DD] [--no-buzz] [--ignore-cutoff] [--no-publish]
"""
import json, os, shutil, subprocess, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import story_cluster as sc

WATCH = sc.WATCH
SITE = r"C:\Users\lilli\Projects\heartbeat-observatory"
OUT = r"C:\Users\lilli\AI-Shared\state\news-missed"
NTFY = r"C:\Users\lilli\AI-Shared\tools\ntfy-say.py"


def short(t, n=90):
    return t if len(t) <= n else t[: n - 1].rstrip() + "..."


def publish_copy(out_path, day):
    """Copy the report into the watch repo (news-missed/D.md) and push it, so the site page /news/desk/ can read it."""
    rel = f"news-missed/{day}.md"
    try:
        os.makedirs(os.path.join(WATCH, "news-missed"), exist_ok=True)
        shutil.copyfile(out_path, os.path.join(WATCH, rel))
        g = lambda *a, t=120: subprocess.run(["git", *a], cwd=WATCH, capture_output=True, text=True, timeout=t)
        try:
            g("pull", "--rebase", "--autostash", "-q", t=150)
        except subprocess.TimeoutExpired:
            pass
        g("add", "--", rel)
        if g("diff", "--cached", "--quiet", "--", rel).returncode == 0:
            return "no change"
        g("commit", "-q", "-m", f"watch: missed-story report {day}", "-m", "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>", "--", rel)
        r = None
        for _ in range(3):
            r = g("push", "-q")
            if r.returncode == 0:
                return "pushed"
            try:
                g("pull", "--rebase", "--autostash", "-q", t=150)
            except subprocess.TimeoutExpired:
                pass
        return "PUSH FAILED: " + r.stderr.strip()[:200]
    except Exception as e:
        return f"git error: {e}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    day = args[0] if args else datetime.now().strftime("%Y-%m-%d")
    nobuzz = "--no-buzz" in sys.argv
    ep_path = os.path.join(SITE, "news", "episodes", f"{day}.json")
    os.makedirs(OUT, exist_ok=True)
    out_path = os.path.join(OUT, f"{day}.md")
    if not os.path.exists(ep_path):
        msg = f"No episode file for {day} ({ep_path}). The show did not publish by the check time."
        open(out_path, "w", encoding="utf-8").write(f"# News missed-story check {day}\n\n{msg}\n")
        if not nobuzz:
            subprocess.run([sys.executable, NTFY, "News: no episode today", f"No episode file for {day} on main at {datetime.now():%H:%M}. The page is looping the last show."], timeout=60)
        print(msg)
        return
    ep = json.load(open(ep_path, encoding="utf-8"))
    sets = sc.seg_word_sets(sc.episode_segments(ep))
    urls = sc.ep_urls(ep)

    cutoff = None if "--ignore-cutoff" in sys.argv else "04:00"
    items = sc.load_candidates(day, hi_today="04:00", scout_cutoff=cutoff)
    clusters, _ = sc.cluster(items)
    late_items = [i for i in sc.wire_items(day) if i["t"] > "04:00"]
    late_clusters, _ = sc.cluster(late_items)

    must_miss, should_miss, single_miss, must_ok, should_ok = [], [], [], [], []
    for c in clusters:
        ok, share = sc.covered(c, sets, urls)
        c["share"] = share
        t = sc.tier(c)
        if ok:
            if t == "must":
                must_ok.append(c)
            elif t == "should":
                should_ok.append(c)
        else:
            (must_miss if t == "must" else should_miss if t == "should" else single_miss).append(c)

    def line(c):
        links = " · ".join(f"{i['outlet']} {i['url']}" for i in c["sources"])
        why = f"{c['n_outlets']} outlets" + (f"; SAFETY WORDS: {', '.join(c['safety'])}" if c["safety"] else "")
        return f"- {c['best']['title']} ({why}; best overlap with any segment {c['share']:.0%}) {links}"

    L = [f"# News missed-story check {day}", "",
         f"Episode checked: news/episodes/{day}.json ({len(ep.get('segments', []))} segments). Run at {datetime.now():%H:%M}.",
         f"Looked at {len(items)} wire + scout lines (wire from yesterday 06:00 through 04:00 today, plus the 3:10 Perplexity scout), grouped into {len(clusters)} stories. Each story is listed once.",
         f"MUST AIR stories (3+ outlets or a safety word): {len(must_ok) + len(must_miss)}, aired {len(must_ok)}, MISSED {len(must_miss)}. SHOULD AIR (2 outlets): {len(should_ok) + len(should_miss)}, aired {len(should_ok)}, not found {len(should_miss)}. One-outlet stories not found: {len(single_miss)} (only the first 20 listed).", "",
         "How it matched (honest version): a story counts as aired if one of its links is an episode source, or one episode segment holds 45% or more of its core words (rare names and numbers count more), or two of its names plus two other key words. Paraphrase can fool this both ways, so a flagged story is a lead for the next writer, not a verdict.", "",
         "## MUST AIR stories that were MISSED" + (" (Jaron was buzzed)" if must_miss and not nobuzz else "")]
    L += [line(c) for c in must_miss] or ["- None."]
    L += ["", "## SHOULD AIR stories not found (2 outlets)"]
    L += [line(c) for c in should_miss[:40]] or ["- None."]
    if len(should_miss) > 40:
        L.append(f"- ... and {len(should_miss) - 40} more.")
    L += ["", "## One-outlet stories not found (first 20; the rest are noise)"]
    L += [f"- {short(c['best']['title'], 120)} ({c['best']['outlet']}) {c['best']['url']}" for c in single_miss[:20]] or ["- None."]
    L += ["", "## MUST AIR stories that aired (listed so the /news/desk/ page can mark them AIRED)"]
    L += [line(c) for c in must_ok] or ["- None."]
    L += ["", "## SHOULD AIR stories that aired"]
    L += [line(c) for c in should_ok] or ["- None."]
    L += ["", "## After the writers' cutoff (wire stories first seen after 04:00; never counted as misses)"]
    late = [c for c in late_clusters if sc.tier(c) in ("must", "should")]
    late.sort(key=lambda c: (not c["safety"], -c["n_outlets"]))
    L += [f"- [{c['first_seen']}] {c['best']['title']} ({c['n_outlets']} outlets{'; SAFETY WORDS: ' + ', '.join(c['safety']) if c['safety'] else ''}) {c['best']['url']}" for c in late[:25]] or ["- None."]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"{day}: stories {len(clusters)}, MUST aired {len(must_ok)}, MUST missed {len(must_miss)}, SHOULD not found {len(should_miss)} -> {out_path}")
    if "--no-publish" not in sys.argv:
        print("watch repo copy:", publish_copy(out_path, day))

    if must_miss and not nobuzz:
        top = must_miss[:3]
        rest = len(must_miss) - len(top)
        body = "Show missed " + "; ".join(f"{short(c['best']['title'], 60)} ({c['n_outlets']} outlets)" for c in top) + (f" + {rest} more" if rest else "") + f". state/news-missed/{day}.md"
        subprocess.run([sys.executable, NTFY, "News: missed story", body], timeout=60)
        print("buzzed Jaron")


if __name__ == "__main__":
    main()
