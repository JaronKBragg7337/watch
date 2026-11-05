"""Morning missed-story check (added 2026-11-05). Registered as "Watch Missed Story Check", daily 08:20 local.

Compares the episode that aired today (site repo news/episodes/D.json) with what the watch saw: Perplexity's scout
(perplexity/D.md), the rolling wire (wire/D.md plus yesterday's wire after 06:00) and the other desks' captures. Writes
C:\\Users\\lilli\\AI-Shared\\state\\news-missed\\D.md. Buzzes Jaron's phone (one plain line) ONLY if something important was
missed; otherwise stays silent.

How matching works (said plainly in every report): no AI, just word overlap. Each candidate story is reduced to its
"signature" words (names, places, numbers and longer words, minus filler). A story counts as COVERED if at least half of its
signature words (names/numbers weighted double) appear anywhere in the episode text, or if its exact URL is one of the
episode's sources. It is MISSED otherwise. A missed story is IMPORTANT only if (a) it matches the safety words
(chemical, biological, nuclear, radiological, WMD, dirty bomb, NTAS, attack on US soil, Indiana/Midwest evacuation), or
(b) it is corroborated: at least 3 different outlets/desks carry a similar story. Wire items first seen after 04:00 are listed
separately ("after the writers' cutoff") and never count as a miss. Overlap can be fooled by paraphrase, so a flagged item is
a lead for a human or the next writer, not a verdict.

Usage: run_missed_check.py [YYYY-MM-DD] [--no-buzz]
"""
import glob, json, os, re, subprocess, sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_wire import safety_hits, canon_url, STOP  # same word lists as the wire hook

WATCH = r"C:\Users\lilli\Projects\watch"
SITE = r"C:\Users\lilli\Projects\heartbeat-observatory"
OUT = r"C:\Users\lilli\AI-Shared\state\news-missed"
NTFY = r"C:\Users\lilli\AI-Shared\tools\ntfy-say.py"
DESKS = ["codex", "claude", "deepseek", "kimi", "grok", "msi"]
FILLER = STOP | set("report reports reportedly according officials official news live updates latest amid over after says said will could would have has had their about more than not but also what how why who when where which while during other another new".split())

ITEM = re.compile(r"^-\s*\[(?P<t>[^\]]*)\]\s*(?:\[(?P<lab>observed|claim|theory)\]\s*)?(?:\[(?P<cls>[a-z-]+)\]\s*)?(?P<rest>.+)$", re.I)
URL = re.compile(r"https?://[^\s)>\]]+")


def sig(text):
    """Signature words: (word -> weight). Capitalised words, numbers weigh 2; other words 4+ letters weigh 1."""
    out = {}
    for m in re.finditer(r"[A-Za-z0-9][A-Za-z0-9'\-]*", text):
        w = m.group(0)
        lw = w.lower().strip("'-")
        if lw in FILLER or len(lw) < 3:
            continue
        heavy = w[0].isupper() or any(c.isdigit() for c in w)
        if not heavy and len(lw) < 5:
            continue
        out[lw] = max(out.get(lw, 0), 2 if heavy else 1)
    return out


def stem(w):
    return re.sub(r"(ing|ed|es|s|ian|ians)$", "", w) if len(w) > 5 else w


def covered_share(s, text_words):
    tot = sum(s.values()) or 1
    got = sum(v for w, v in s.items() if w in text_words or stem(w) in text_words)
    return got / tot


def parse_items(path, source_label):
    items = []
    if not os.path.exists(path):
        return items
    for ln in open(path, encoding="utf-8", errors="ignore"):
        m = ITEM.match(ln.strip())
        if not m:
            continue
        rest = m.group("rest")
        urls = URL.findall(rest)
        title = re.split(r"\s+[\u2014-]\s+https?://", rest)[0]
        title = re.sub(r"\s+[\u2014-]\s+[^\u2014]*$", "", title) if "\u2014" in title else title
        title = re.sub(r"^(?:(?:observed|claim|theory)\s+)?(?:(?:official|press|solo|social|model-only)\s+)?", "", title.strip(), flags=re.I)
        if len(title) < 15:
            continue
        items.append({"title": title.strip(), "urls": urls, "t": m.group("t"), "src": source_label, "label": m.group("lab") or "", "cls": m.group("cls") or ""})
    return items


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    day = args[0] if args else datetime.now().strftime("%Y-%m-%d")
    yday = (datetime.strptime(day, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    ep_path = os.path.join(SITE, "news", "episodes", f"{day}.json")
    os.makedirs(OUT, exist_ok=True)
    out_path = os.path.join(OUT, f"{day}.md")
    if not os.path.exists(ep_path):
        msg = f"No episode file for {day} ({ep_path}). The show did not publish by the check time."
        open(out_path, "w", encoding="utf-8").write(f"# News missed-story check {day}\n\n{msg}\n")
        if "--no-buzz" not in sys.argv:
            subprocess.run([sys.executable, NTFY, "News: no episode today", f"No episode file for {day} on main at {datetime.now():%H:%M}. The page is looping the last show."], timeout=60)
        print(msg)
        return
    ep = json.load(open(ep_path, encoding="utf-8"))
    ep_text = json.dumps(ep, ensure_ascii=False)
    strings = []

    def walk(o):
        if isinstance(o, str):
            if not o.startswith("http"):
                strings.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(ep)
    ep_text_plain = " ".join(strings)
    ep_words = {w.lower().strip("'-") for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", ep_text_plain)}
    ep_words |= {stem(w) for w in ep_words}
    ep_urls = {canon_url(u) for u in URL.findall(ep_text)}

    # candidates
    pp_path = os.path.join(WATCH, "perplexity", f"{day}.md")
    cands = parse_items(pp_path, "perplexity")
    wire_late = []
    pp_time = ""
    if os.path.exists(pp_path):
        mt = re.search(r"Time:\s*(\d\d:\d\d)", open(pp_path, encoding="utf-8", errors="ignore").read(600))
        pp_time = mt.group(1) if mt else ""
    if pp_time >= "04:00" and "--ignore-cutoff" not in sys.argv:  # the scout ran after the writers (a manual run): its items could not have been used
        for it in cands:
            it["t"] = pp_time
        wire_late, cands = cands, []
    for d, cut_lo in ((yday, "06:00"), (day, "00:00")):
        for it in parse_items(os.path.join(WATCH, "wire", f"{d}.md"), "wire"):
            m = re.match(r"(\d\d:\d\d)", it["t"])
            if not m or m.group(1) < cut_lo:
                continue
            if d == day and m.group(1) >= "04:00":
                wire_late.append(it)
            else:
                cands.append(it)
    # corroboration pool: every desk + wire + perplexity
    pool = []
    for d in DESKS:
        pool += parse_items(os.path.join(WATCH, d, f"{day}.md"), d)
    pool += parse_items(os.path.join(WATCH, "grok", f"{day}-gaps.md"), "grok-gaps")
    pool += cands + wire_late
    pool_sigs = [(p, set(sig(p["title"]))) for p in pool]

    def outlet(p):
        for u in p["urls"][:1]:
            m = re.match(r"https?://(?:www\.)?([^/]+)", u)
            if m:
                return m.group(1)
        return p["src"]

    def corroboration(it):
        a = set(sig(it["title"]))
        if len(a) < 3:
            return 1
        who = {outlet(it) + "|" + it["src"]}
        for p, b in pool_sigs:
            if p is it or not b:
                continue
            if len(a & b) / min(len(a), len(b)) >= 0.5 and len(a & b) >= 3:
                who.add(outlet(p) + "|" + p["src"])
        return len({w.split("|")[0] for w in who})

    seen_keys, covered, missed, important = set(), [], [], []
    for it in cands:
        key = " ".join(sorted(sig(it["title"]))[:8])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        s = sig(it["title"])
        share = covered_share(s, ep_words)
        url_hit = any(canon_url(u) in ep_urls for u in it["urls"])
        it["share"] = share
        if url_hit or share >= 0.5:
            covered.append(it)
            continue
        it["safety"] = safety_hits(it["title"])
        it["corr"] = corroboration(it)
        missed.append(it)
        if it["safety"] or it["corr"] >= 3:
            important.append(it)
    late_missed = []
    for it in wire_late:
        s = sig(it["title"])
        if not (canon_url(it["urls"][0]) in ep_urls if it["urls"] else False) and covered_share(s, ep_words) < 0.5:
            it["safety"] = safety_hits(it["title"])
            late_missed.append(it)

    n_perp = sum(1 for c in cands if c["src"] == "perplexity")
    L = [f"# News missed-story check {day}", "",
         f"Episode checked: news/episodes/{day}.json ({len(ep.get('segments', []))} segments). Run at {datetime.now():%H:%M}.",
         f"Candidates looked at: {len(cands)} unique stories ({n_perp} from Perplexity's scout, {len(cands) - n_perp} from the rolling wire, yesterday 06:00 on through 04:00 today).",
         f"Covered: {len(covered)}. Not found in the episode: {len(missed)}. Important misses: {len(important)}.", "",
         "How it matched (honest version): word overlap only. A story is COVERED if half or more of its signature words (names and numbers count double) appear anywhere in the episode, or its URL is an episode source. Paraphrase or a different spelling can make a covered story look missed, and a loose overlap can hide a real miss. IMPORTANT = matches a safety word, or at least 3 different outlets carry a similar story.", ""]
    L.append("## Important misses (Jaron was buzzed)" if important and "--no-buzz" not in sys.argv else "## Important misses")
    if important:
        for it in important:
            why = ("safety words: " + ", ".join(it["safety"])) if it["safety"] else f"{it['corr']} outlets carry it"
            L.append(f"- {it['title']} ({why}; overlap {it['share']:.0%}; {it['src']}) {it['urls'][0] if it['urls'] else ''}")
    else:
        L.append("- None.")
    L += ["", "## Other stories not found in the episode (single-source or low importance)"]
    rest = [m for m in missed if m not in important]
    L += [f"- {it['title']} (overlap {it['share']:.0%}; {it['src']}; {it['corr']} outlet(s)) {it['urls'][0] if it['urls'] else ''}" for it in rest[:40]] or ["- None."]
    if len(rest) > 40:
        L.append(f"- ... and {len(rest) - 40} more.")
    L += ["", "## After the writers' cutoff (wire items first seen after 04:00; never counted as misses)"]
    L += [f"- [{it['t']}] {it['title']} {'(SAFETY WORDS: ' + ', '.join(it['safety']) + ')' if it['safety'] else ''} {it['urls'][0] if it['urls'] else ''}" for it in sorted(late_missed, key=lambda x: not x["safety"])[:40]] or ["- None."]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"{day}: candidates {len(cands)}, covered {len(covered)}, missed {len(missed)}, important {len(important)} -> {out_path}")

    if important and "--no-buzz" not in sys.argv:
        top = important[0]["title"][:110]
        body = f"The show may have missed {len(important)} important stor{'y' if len(important) == 1 else 'ies'}: {top}. Details: state/news-missed/{day}.md"
        subprocess.run([sys.executable, NTFY, "News: possible missed story", body], timeout=60)
        print("buzzed Jaron")


if __name__ == "__main__":
    main()
