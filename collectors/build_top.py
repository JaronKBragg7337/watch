"""Must-cover list for the daily news writers (added 2026-11-06).

Reads the rolling wire (yesterday 06:00 on through now) and today's Perplexity scout, clusters the lines into STORIES
(collectors/story_cluster.py), counts distinct outlets per story and writes watch/wire/YYYY-MM-DD-top.md:
  MUST AIR   = carried by 3+ distinct outlets, or matches a safety word (chemical, nuclear, NTAS, ...)
  SHOULD AIR = carried by 2 outlets
Each story is one line: outlet count, best headline, best 2 sources. Writers (cloud 3:45 writer, backup run_news.ps1,
Grok gap check) read it FIRST; every MUST AIR story gets covered, briefly if need be.

Runs: Windows task "Watch Top Stories" daily 03:33 local (commits + pushes the file itself), and as the tail of every
rolling-wire run (file only; the wire's own hourly push carries it).

Usage: build_top.py [YYYY-MM-DD] [--until HH:MM] [--no-push]
No AI and no network. Honest limit: word overlap, so an unusual paraphrase can split one story in two (it then shows as two
smaller stories) and two different stories can rarely be glued together. Counts are a floor, not a verdict.
"""
import os, sys, json, subprocess
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import story_cluster as sc

WATCH = sc.WATCH
SITE = r"C:\Users\lilli\Projects\heartbeat-observatory"
SHOULD_CAP = 40


def aired_yesterday(clusters, day):
    """Mark stories whose words are already in yesterday's episode (a follow-up needs only the NEW development)."""
    yday = (datetime.strptime(day, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    p = os.path.join(SITE, "news", "episodes", f"{yday}.json")
    if not os.path.exists(p):
        return
    try:
        ep = json.load(open(p, encoding="utf-8"))
    except Exception:
        return
    sets = sc.seg_word_sets(sc.episode_segments(ep))
    urls = sc.ep_urls(ep)
    for c in clusters:
        c["aired_yday"] = sc.covered(c, sets, urls)[0]


def build(day, until="23:59", write=True):
    items = sc.load_candidates(day, hi_today=until, scout_cutoff=None)
    clusters, _ = sc.cluster(items)
    aired_yesterday([c for c in clusters if sc.tier(c) != "single"], day)
    must = [c for c in clusters if sc.tier(c) == "must"]
    should = [c for c in clusters if sc.tier(c) == "should"]

    def line(c):
        src = " · ".join(f"{i['outlet']} {i['url']}" for i in c["sources"]) or "(no direct link)"
        extra = ""
        if c["safety"]:
            extra += f" SAFETY WORDS: {', '.join(c['safety'])}."
        if c.get("aired_yday"):
            extra += " (Looks like it aired yesterday: cover only what is NEW today.)"
        return f"- [{c['n_outlets']} outlets] {c['best']['title']} — {src}{extra}"

    L = [f"# Must-cover list — {day}",
         f"Built {datetime.now():%H:%M} from {len(items)} wire + scout lines (wire from yesterday 06:00 through {until if until != '23:59' else 'now'}, plus today's Perplexity scout), grouped into {len(clusters)} stories.",
         "Rule: every MUST AIR story gets covered in the show, briefly if it is small. SHOULD AIR stories get a line or a spot in Quick Hits when there is room. A bigger news day means a longer show (Jaron's rule). Labels and honesty rules in WRITER.md still apply: label claims, invent nothing; the sources on each line are where to check.",
         "How it was built (plain): lines about the same story are grouped by shared names and key words; outlets are counted once each (a Google News item counts as the outlet it names). MUST AIR = 3 or more different outlets, or a safety word (chemical, biological, nuclear, radiological, WMD, dirty bomb, NTAS, attack on US soil, Midwest evacuation). Word overlap can split one story into two smaller ones or, rarely, join two; treat counts as a floor.", "",
         f"## MUST AIR ({len(must)})"]
    L += [line(c) for c in must] or ["- None."]
    L += ["", f"## SHOULD AIR ({len(should)})"]
    L += [line(c) for c in should[:SHOULD_CAP]] or ["- None."]
    if len(should) > SHOULD_CAP:
        L.append(f"- ... and {len(should) - SHOULD_CAP} more 2-outlet stories in the wire.")
    text = "\n".join(L) + "\n"
    if write:
        os.makedirs(os.path.join(WATCH, "wire"), exist_ok=True)
        open(os.path.join(WATCH, "wire", f"{day}-top.md"), "w", encoding="utf-8").write(text)
    return text, must, should


def git(*a, t=120):
    return subprocess.run(["git", *a], cwd=WATCH, capture_output=True, text=True, timeout=t)


def push(day):
    rel = f"wire/{day}-top.md"
    try:
        try:
            git("pull", "--rebase", "--autostash", "-q", t=150)
        except subprocess.TimeoutExpired:
            pass   # push still works if the pull was slow; a rejected push retries below
        git("add", "--", rel)
        if git("diff", "--cached", "--quiet", "--", rel).returncode == 0:
            return "no change"
        git("commit", "-q", "-m", f"watch: must-cover list {day}", "-m", "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>", "--", rel)
        for _ in range(3):
            r = git("push", "-q")
            if r.returncode == 0:
                return "pushed"
            try:
                git("pull", "--rebase", "--autostash", "-q", t=150)
            except subprocess.TimeoutExpired:
                pass
        return "PUSH FAILED: " + r.stderr.strip()[:200]
    except Exception as e:
        return f"git error: {e}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    day = args[0] if args else datetime.now().strftime("%Y-%m-%d")
    until = "23:59"
    if "--until" in sys.argv:
        until = sys.argv[sys.argv.index("--until") + 1]
        args = [a for a in args if a != until]
        day = args[0] if args else day
    text, must, should = build(day, until)
    status = "no push" if "--no-push" in sys.argv else push(day)
    print(f"{day}: must {len(must)}, should {len(should)} -> wire/{day}-top.md ({status})")
    log = os.path.join(WATCH, "collectors", "top_runs.log")
    open(log, "a", encoding="utf-8").write(f"{datetime.now():%Y-%m-%d %H:%M} top: must {len(must)}, should {len(should)}, {status}\n")


if __name__ == "__main__":
    main()
