"""Shared story clustering for the daily news watch (added 2026-11-06).

Why: on 11/6 the show skipped Newsom commuting 548 death sentences (7 outlets), Russell Brand's conviction (4+) and more,
because the writers faced ~660 raw wire lines. This module turns raw lines (wire + Perplexity scout) into STORIES with an
outlet count, so build_top.py can hand the writers a short MUST-AIR list and run_missed_check.py can list each story once.

No AI, no network: plain word overlap, weighted so rare words (names, numbers) count more than common ones.
  1. normalise a title into stemmed content words; drop filler;
  2. weight each word by how rare it is across the day's lines (IDF);
  3. two lines are the same story when their shared rare words are a big share of the shorter line's weight;
  4. greedy clustering (a line joins the cluster it matches best on average, never by one stray shared word);
  5. count DISTINCT outlets per cluster (Google News "X via Google News" counts as X; Perplexity "(domain)" counts as the domain).
Roundup lines ("Morning Rundown", "First Thing", "Up First", ...) are left out: they mention many stories and would glue
unrelated clusters together.
"""
import json, math, os, re
from datetime import datetime, timedelta

from run_wire import safety_hits, canon_url, STOP  # same safety words as the wire hook

WATCH = r"C:\Users\lilli\Projects\watch"

FILLER = STOP | set("""report reports reported reportedly according officials official news live updates latest amid over after says said will
could would have has had their about more than not but also what how why who when where which while during other another new
with that this from into out off up down just still first one two year years day days week today tonight yesterday world
us u.s. first thing here whats what's why how watch video photos photo analysis opinion explainer""".split())
ROUNDUP = re.compile(r"morning rundown|first thing|up first|while you were sleeping|morning briefing|newsletter|\bday ?ahead\b|"
                     r"stories you might have missed|top stories|what to know|live updates|evening briefing|daily briefing|"
                     r"world in brief|headlines at|news summary|summary\s*brief|hourly summary|podcast|\bquiz\b", re.I)
MONTHS = set("january february march april may june july august september october november december monday tuesday wednesday thursday friday saturday sunday".split())
# a few words that are the same story in different outlets' language
ALIAS = {"convicted": "guilty", "convict": "guilty", "conviction": "guilty", "commutes": "commut", "resigns": "resign",
         "steps": "resign", "quits": "resign", "resignation": "resign", "kills": "kill", "killed": "kill", "dead": "kill",
         "dies": "kill", "died": "kill", "sentences": "sentenc", "sentence": "sentenc", "troops": "troop", "soldiers": "troop"}


def stem(w):
    w = w.lower().replace("\u2019", "'")
    if w.endswith("'s"):
        w = w[:-2]
    w = w.strip("'-")
    if w in ALIAS:
        return ALIAS[w]
    if len(w) > 4:
        for suf in ("ies", "ing", "ed", "es", "s"):
            if w.endswith(suf):
                w = w[: -len(suf)] + ("y" if suf == "ies" else "")
                break
        if w.endswith("e") and len(w) > 4:
            w = w[:-1]
    return ALIAS.get(w, w)


def words(title):
    """List of (stem, is_name). A name = capitalised word that is not the first word of the title."""
    out = []
    raw = re.findall(r"[A-Za-z0-9][A-Za-z0-9'\u2019\-\.]*[A-Za-z0-9]|[A-Za-z0-9]", title)
    for i, w in enumerate(raw):
        lw = w.lower().strip(".'\u2019-")
        if lw in FILLER or lw in MONTHS or len(lw) < 3 and not lw.isdigit():
            continue
        name = (i > 0 and w[0].isupper() and not w.isupper() or (w.isupper() and len(w) > 2 and i > 0)) or any(c.isdigit() for c in w)
        if i == 0 and w[0].isupper() and not w.isupper():
            name = True   # first word: could be a name (Marco Rubio ...); the merge step only trusts RARE ones
        out.append((stem(lw), bool(name)))
    return out


# ---------------------------------------------------------------- outlets
OUTLET_ALIAS = {"theguardian": "guardian", "guardian": "guardian", "bbcnews": "bbc", "bbc": "bbc", "cbsnews": "cbs", "cbs": "cbs",
                "nbcnews": "nbc", "nbc": "nbc", "abcnews": "abc", "abcnewsgo": "abc", "abc": "abc", "abc7": "abc7", "abc7news": "abc7",
                "aljazeera": "aljazeera", "japantimes": "japantimes", "dw": "dw", "dwcom": "dw", "apnews": "ap", "ap": "ap",
                "associatedpress": "ap", "reuters": "reuters", "afp": "afp", "france24": "france24", "cnbc": "cnbc", "npr": "npr",
                "nytimes": "nyt", "newyorktimes": "nyt", "washingtonpost": "wapo", "washpost": "wapo", "timesofisrael": "timesofisrael",
                "englishnewscn": "xinhua", "xinhuanet": "xinhua", "news": "xinhua", "cnn": "cnn", "politico": "politico",
                "thehill": "thehill", "bbcco": "bbc", "bbccouk": "bbc", "straitstimes": "straitstimes", "aa": "anadolu", "aacomtr": "anadolu", "mobilaacomtr": "anadolu"}


def norm_outlet(name):
    n = (name or "").strip()
    if not n:
        return "?"
    m = re.match(r"^Perplexity \((.+)\)$", n)
    if m:
        n = m.group(1)
    if " via " in n:
        left, right = n.rsplit(" via ", 1)
        n = left if re.search(r"google news", right, re.I) else right
        if "," in n:   # "(c) Name, Reuters via France 24" -> keep the outlet that carried it
            n = n.split(",")[-1]
    n = n.lower()
    n = re.sub(r"[^a-z0-9. ]", "", n)
    n = re.sub(r"^(www|english|mobil|m|amp)\.", "", n)
    n = re.sub(r"\.(com|org|net|co\.uk|co\.jp|co\.in|com\.au|com\.tr|gov|cn|uk|jp|tr)$", "", n)
    n = n.replace(".", "").replace(" ", "")
    n = re.sub(r"^the", "", n) if n not in ("theguardian",) else n
    n = re.sub(r"(world|intl|us|news)$", "", n) if len(n) > 7 and n not in OUTLET_ALIAS else n
    return OUTLET_ALIAS.get(n, n) or "?"


def url_outlet(u):
    m = re.match(r"https?://([^/]+)", u or "")
    return norm_outlet(m.group(1)) if m else "?"


# ---------------------------------------------------------------- loading
ITEM = re.compile(r"^-\s*\[(?P<t>[^\]]*)\]\s*(?:\[(?P<lab>observed|claim|theory)\]\s*)?(?:\[(?P<cls>[a-z-]+)\]\s*)?(?P<rest>.+)$", re.I)
URL = re.compile(r"https?://[^\s)>\]]+")


def scout_items(path):
    items = []
    if not os.path.exists(path):
        return items
    head = open(path, encoding="utf-8", errors="ignore").read(600)
    mt = re.search(r"Time:\s*(\d\d:\d\d)", head)
    t = mt.group(1) if mt else "00:00"
    for ln in open(path, encoding="utf-8", errors="ignore"):
        m = ITEM.match(ln.strip())
        if not m:
            continue
        rest = m.group("rest")
        urls = URL.findall(rest)
        title = re.split(r"\s+[\u2014-]\s+https?://", rest)[0]
        title = re.sub(r"^(?:(?:observed|claim|theory)\s+)?(?:(?:official|press|solo|social|model-only)\s+)?", "", title.strip(), flags=re.I)
        if len(title) < 15:
            continue
        out = url_outlet(urls[0]) if urls else "perplexity"
        items.append({"title": title.strip(), "url": urls[0] if urls else "", "t": t, "src": "scout", "outlet": out,
                      "label": m.group("lab") or "", "cls": m.group("cls") or ""})
    return items


def wire_items(day):
    items = []
    p = os.path.join(WATCH, "wire", f"{day}.jsonl")
    if not os.path.exists(p):
        return items
    for ln in open(p, encoding="utf-8", errors="ignore"):
        try:
            r = json.loads(ln)
        except Exception:
            continue
        title = (r.get("title") or "").strip()
        if len(title) < 15:
            continue
        items.append({"title": title, "url": r.get("url", ""), "t": r.get("seen", "00:00"), "src": "wire",
                      "outlet": norm_outlet(r.get("source", "")), "label": r.get("label", ""), "cls": r.get("cls", ""),
                      "raw_source": r.get("source", "")})
    return items


def load_candidates(day, hi_today="23:59", lo_yesterday="06:00", use_scout=True, scout_cutoff=None):
    """Wire from yesterday `lo_yesterday` through today `hi_today`, plus today's scout. Returns a list of items."""
    yday = (datetime.strptime(day, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    out = [i for i in wire_items(yday) if i["t"] >= lo_yesterday]
    out += [i for i in wire_items(day) if i["t"] <= hi_today]
    if use_scout:
        sc = scout_items(os.path.join(WATCH, "perplexity", f"{day}.md"))
        if scout_cutoff and sc and sc[0]["t"] > scout_cutoff:
            sc = []
        out += sc
    return out


# ---------------------------------------------------------------- clustering
def _prep(items):
    live = []
    for it in items:
        if ROUNDUP.search(it["title"]):
            it["roundup"] = True
            continue
        it["w"] = words(it["title"])
        it["set"] = {s for s, _ in it["w"]}
        if len(it["set"]) >= 3:
            live.append(it)
    df = {}
    for it in live:
        for s in it["set"]:
            df[s] = df.get(s, 0) + 1
    n = max(len(live), 1)
    idf = {s: math.log(1 + n / c) for s, c in df.items()}
    return live, idf


def _score(a, b, idf):
    """Shared weight as a fraction of the lighter line's weight; needs 2+ shared words, one of them rare."""
    sh = a & b
    if len(sh) < 2:
        return 0.0
    wsh = sum(idf.get(s, 1) for s in sh)
    if max(idf.get(s, 1) for s in sh) < 2.2 and len(sh) < 3:   # only common words in common
        return 0.0
    return wsh / (min(sum(idf.get(s, 1) for s in a), sum(idf.get(s, 1) for s in b)) or 1)


NAME_IDF = 3.2


def cluster(items, thresh=0.5):
    live, idf = _prep(items)
    clusters = []
    for it in sorted(live, key=lambda x: -len(x["set"])):
        best, bs = None, 0.0
        for c in clusters:
            scores = sorted((_score(it["set"], m["set"], idf) for m in c["items"]), reverse=True)
            # best match, but a cluster of 3+ also needs the second-best to agree a little (no chaining by one stray line)
            s = scores[0] if len(scores) < 3 else (scores[0] + scores[1]) / 2
            if s > bs:
                best, bs = c, s
        if best is not None and bs >= thresh:
            best["items"].append(it)
        else:
            clusters.append({"items": [it]})
    # merge pass: two clusters whose cores match
    changed = True
    while changed:
        changed = False
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                a, b = clusters[i], clusters[j]
                sa = sorted((_score(x["set"], y["set"], idf) for x in a["items"] for y in b["items"]), reverse=True)
                na = {s for x in a["items"] for s, nm in x["w"] if nm and idf.get(s, 0) >= NAME_IDF}
                nb = {s for x in b["items"] for s, nm in x["w"] if nm and idf.get(s, 0) >= NAME_IDF}
                if len(na & nb) >= 2 and len(a["items"]) + len(b["items"]) <= 6 and sa and sa[0] >= 0.3:   # same two rare names (Marco Rubio, Russell Brand) = same story
                    a["items"] += b["items"]
                    del clusters[j]
                    changed = True
                    break
                if sa and sa[0] >= max(thresh, 0.6) and (len(sa) < 6 or sa[min(2, len(sa) - 1)] >= thresh * 0.8):
                    a["items"] += b["items"]
                    del clusters[j]
                    changed = True
                    break
            if changed:
                break
    for c in clusters:
        _describe(c, idf)
    clusters.sort(key=lambda c: (-c["n_outlets"], -len(c["items"])))
    return clusters, idf


PREF = ["bbc", "guardian", "npr", "cbs", "nbc", "abc", "aljazeera", "france24", "cnbc", "dw", "timesofisrael", "japantimes",
        "ap", "reuters", "afp", "nyt", "wapo", "politico", "cnn", "thehill"]


def _describe(c, idf):
    its = c["items"]
    c["outlets"] = sorted({i["outlet"] for i in its if i["outlet"] != "?"})
    c["n_outlets"] = len(c["outlets"])
    c["safety"] = sorted({h for i in its for h in safety_hits(i["title"])})
    # core words: in at least 2 lines (or the only line), heaviest first
    cnt = {}
    for i in its:
        for s in i["set"]:
            cnt[s] = cnt.get(s, 0) + 1
    need = 2 if len(its) >= 3 else 1
    core = {s for s, k in cnt.items() if k >= need}
    names = {s for i in its for s, nm in i["w"] if nm}
    c["core"] = {s: idf.get(s, 1) * (1.5 if s in names else 1.0) for s in core}
    c["names"] = core & names

    tot = sum(c["core"].values()) or 1

    def bad_url(i):
        u = (i["url"] or "").lower().replace("-", " ").replace("_", " ")
        return 1 if (not u or "news.google.com" in u or ROUNDUP.search(u) or "liveblog" in u) else 0

    def pref(i):
        return PREF.index(i["outlet"]) if i["outlet"] in PREF else 50

    def rank(i):   # best headline: carries most of the story's core words, short, from a recognised outlet
        share = sum(w for s, w in c["core"].items() if s in i["set"]) / tot
        return (-round(share * 4) / 4, len(i["title"]) > 120, i["src"] == "scout", pref(i), abs(len(i["title"]) - 75))

    def src_rank(i):   # best links: a direct page, not a roundup, from a recognised outlet
        return (bad_url(i), i["src"] == "scout", pref(i))
    c["best"] = sorted(its, key=rank)[0]
    seen, srcs = set(), []
    for i in sorted(its, key=src_rank):
        if i["outlet"] in seen or not i["url"]:
            continue
        seen.add(i["outlet"])
        srcs.append(i)
        if len(srcs) == 2:
            break
    c["sources"] = srcs
    c["first_seen"] = min(i["t"] for i in its)


def tier(c):
    if c["safety"] or c["n_outlets"] >= 3:
        return "must"
    if c["n_outlets"] == 2:
        return "should"
    return "single"


# ---------------------------------------------------------------- matching a story against an episode
def episode_segments(ep):
    """Text blobs: one per segment (plus the ticker as its own blob); URLs excluded."""
    def walk(o, acc):
        if isinstance(o, str):
            if not o.startswith("http"):
                acc.append(o)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k in ("sources", "url", "id", "kind", "graphic"):
                    continue
                walk(v, acc)
        elif isinstance(o, list):
            for v in o:
                walk(v, acc)
    blobs = []
    for s in ep.get("segments", []):
        acc = []
        walk(s, acc)
        blobs.append(" ".join(acc))
    t = []
    walk(ep.get("ticker", []), t)
    blobs.append(" ".join(t))
    return blobs


def ep_urls(ep):
    return {canon_url(u) for u in URL.findall(json.dumps(ep, ensure_ascii=False))}


def covered(c, seg_sets, urls):
    """(is_covered, best_share). Covered if any member URL is an episode source, or a single segment holds >=45% of the
    story's core weight, or holds 2+ of its names plus 2+ other core words (names and key nouns together)."""
    for i in c["items"]:
        if i["url"] and canon_url(i["url"]) in urls:
            return True, 1.0
    core, names = c["core"], c["names"]
    tot = sum(core.values()) or 1
    best = 0.0
    for ss in seg_sets:
        got = {s for s in core if s in ss}
        share = sum(core[s] for s in got) / tot
        best = max(best, share)
        if share >= 0.45:
            return True, share
        gn = got & names
        if len(gn) >= 2 and len(got - gn) >= 2:
            return True, max(share, 0.45)
    return False, best


def seg_word_sets(blobs):
    return [{s for s, _ in words(b)} | {s for s, _ in words(b.lower())} for b in blobs]
