"""Rolling wire for the daily watch (added 2026-11-05).

Why: the nightly captures are one 3 AM snapshot; on 11/4-11/5 the internet dropped around 3-4 AM and most desks never wrote.
The wire keeps a running, deduplicated list of new stories all day so the 3:45 / 4:20 writers (and the 8:20 missed-story
check) always have fresh material, even when a desk fails.

Registered as Windows task "Watch Rolling Wire": hourly at :28 (3:28 lands just before the 3:35 gap check and the 3:45 writer).
  - every run: free RSS/Atom feeds (one failed feed never stops the run)
  - every 3 hours (00, 03, 06 ... 21 local): ONE broad Perplexity Sonar question (about $0.005-0.01; hard monthly cap below)
  - new items only (dedupe by canonical URL and near-identical title, today + yesterday) -> wire/YYYY-MM-DD.md
  - safety hook: chemical / biological / nuclear / radiological / WMD / dirty bomb / DHS-NTAS / attack on US soil /
    Indiana-Midwest evacuation or shelter -> one mailbox note per item to satya-twin and claude. Satya decides the level;
    this script never touches the safety signal and never drops a threat item.
  - commits only wire/ and pushes, at most once an hour.

Usage: run_wire.py [--no-push] [--no-perplexity] [--force-perplexity] [--no-alerts]
Key: PERPLEXITY_API_KEY in ~/.secrets/keys.env (never printed).
"""
import hashlib, html, json, os, re, subprocess, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

WATCH = r"C:\Users\lilli\Projects\watch"
WIRE = os.path.join(WATCH, "wire")
STATE = os.path.join(WATCH, "collectors", "wire_state.json")
MAILBOX = r"C:\Users\lilli\AI-Shared\tools\mailbox.py"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"

NOW = datetime.now()
DAY = NOW.strftime("%Y-%m-%d")
YDAY = (NOW - timedelta(days=1)).strftime("%Y-%m-%d")
FEED_WINDOW_H = 6          # only items published in the last 6 hours (hourly runs, so plenty of overlap)
PER_FEED_CAP = 12          # newest N per feed per run, keeps the day's file readable
PPLX_MONTH_CAP = 1.40      # dollars; the wire's own Perplexity budget is about $1.50 a month
ALERT_MAX_INDIVIDUAL = 8   # per run; anything beyond goes in ONE rollup note (nothing is dropped)
ALERT_WINDOW_H = 8         # only alert on items published in the last 8 hours (first run must not replay old news)

# (name, url, class). AP, Reuters and ISW direct feeds were dead/403 on 2026-11-05; they come via Google News (11/6).
FEEDS = [
    ("AP (via Google News)", "https://news.google.com/rss/search?q=site:apnews.com+when:1d&hl=en-US&gl=US&ceid=US:en", "press"),
    ("Reuters (via Google News)", "https://news.google.com/rss/search?q=site:reuters.com+when:1d&hl=en-US&gl=US&ceid=US:en", "press"),
    ("ISW (via Google News)", "https://news.google.com/rss/search?q=site:understandingwar.org+when:7d&hl=en-US&gl=US&ceid=US:en", "press"),
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml", "press"),
    ("NPR", "https://feeds.npr.org/1004/rss.xml", "press"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml", "press"),
    ("The Guardian World", "https://www.theguardian.com/world/rss", "press"),
    ("DW", "https://rss.dw.com/rdf/rss-en-world", "press"),
    ("France 24", "https://www.france24.com/en/rss", "press"),
    ("NBC News", "https://feeds.nbcnews.com/nbcnews/public/news", "press"),
    ("CBS News World", "https://www.cbsnews.com/latest/rss/world", "press"),
    ("ABC News Intl", "https://abcnews.go.com/abcnews/internationalheadlines", "press"),
    ("CNBC", "https://www.cnbc.com/id/100727362/device/rss/rss.html", "press"),
    ("Times of Israel", "https://www.timesofisrael.com/feed/", "press"),
    ("Japan Times", "https://www.japantimes.co.jp/feed/", "press"),
    ("Google News World", "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en", "press"),
    ("Google News US", "https://news.google.com/rss/headlines/section/topic/NATION?hl=en-US&gl=US&ceid=US:en", "press"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index", "press"),
    ("The Verge", "https://www.theverge.com/rss/index.xml", "press"),
    ("OpenAI", "https://openai.com/news/rss.xml", "official"),
    # official sources speaking for themselves
    ("US State Dept", "https://www.state.gov/rss-feed/press-releases/feed/", "official"),
    ("State Dept travel advisories", "https://travel.state.gov/_res/rss/TAsTWs.xml", "official"),
    ("CISA cyber advisories", "https://www.cisa.gov/cybersecurity-advisories/all.xml", "official"),
    ("US Defense Dept", "https://www.defense.gov/DesktopModules/ArticleCS/RSS.ashx?ContentType=1&Site=945&max=10", "official"),
    ("White House", "https://www.whitehouse.gov/news/feed/", "official"),
    ("Federal Reserve", "https://www.federalreserve.gov/feeds/press_all.xml", "official"),
    ("WHO news", "https://www.who.int/rss-feeds/news-english.xml", "official"),
    ("NWS extreme alerts", "https://api.weather.gov/alerts/active.atom?status=actual&severity=Extreme", "official"),
]

DOMAINS = [
    "01 crypto / on-chain / stablecoins", "02 stocks / macro / rates / labor", "03 AI / models / infra / pricing of intelligence",
    "04 energy / grid / compute power / materials", "05 geopolitics / conflict / borders / law", "06 companies / hiring / M&A / who is shipping",
    "07 demographics / migration / prices on the ground / culture", "08 supply chain / freight / food / housing inputs",
    "09 prediction-market resolution events", "10 crypto / stock catalysts", "11 major US cities and regions", "12 sports",
    "13 U.S. politics and elections", "14 weather, climate and disasters", "15 health", "16 law, courts and regulation",
    "17 outages and cyber", "18 disclosure and anomalies", "19 science and space", "20 entertainment and culture markets", "21 uncategorised",
]
DOMAIN_RULES = [  # same order and patterns as Get-Domain in run_msi.ps1, plus election/politics
    (5, r"iran|israel|ukrain|russia|\bwar\b|missile|gaza|venezuela|greenland|border|ceasefire|\bnato\b|military|attack|troops|diplomat|hezbollah|houthi|strike"),
    (1, r"bitcoin|crypto|ethereum|stablecoin|blockchain|coinbase|token"),
    (2, r"\bstocks?\b|\bmarkets?\b|\bfed\b|federal reserve|inflation|jobs report|treasury|interest rate|economy|payroll|dow |nasdaq|central bank"),
    (3, r"openai|anthropic|artificial intelligence|\bai\b|chatgpt|claude|chip|data center|cloud computing"),
    (4, r"\boil\b|energy|power grid|electricity|solar|nuclear|gas prices|battery|lithium|brent"),
    (6, r"company|business|earnings|merger|layoff|\bceo\b|launches|revenue|acquisition"),
    (13, r"election|midterm|congress|senate|white house|trump|democrat|republican|poll"),
    (17, r"hack|cyber|outage|breach|ransomware|internet down|cloudflare"),
    (14, r"weather|storm|hurricane|flood|wildfire|earthquake|climate|tornado|tsunami"),
    (15, r"health|virus|outbreak|\bfda\b|vaccine|hospital|drug approval|\bwho\b|ebola|measles"),
    (16, r"court|judge|lawsuit|ruling|regulation|\bsec\b|\bfcc\b|bill signed"),
    (19, r"nasa|\bspace\b|rocket|satellite|astronom|planet"),
    (12, r"\bsport|\bnfl\b|\bnba\b|\bmlb\b|\bnhl\b|soccer|world cup|olympic"),
    (20, r"\bfilm\b|movie|music|album|box office|streaming|actor|award"),
    (8, r"supply chain|shipping|freight|\bfood\b|grain|\bport\b|factory|housing"),
    (7, r"migration|prices|cost of living|population|culture"),
]

# ---- safety hook -----------------------------------------------------------------------------------------------
SAFETY = [
    ("chemical", r"\bchemical"),
    ("biological", r"\bbiological|\bbioweapon|\bbio-?terror|\banthrax\b"),
    # 11/5: bare "nuclear" flagged cost/diplomacy stories (Fukushima bill, Iran proposals). Keep anything that reads as a
    # threat or an accident: weapons, strikes, tests, launches, leaks, radiation, alerts, attacks on plants.
    ("nuclear", r"\bnuclear\b.{0,60}\b(weapon|warhead|bomb|strike|attack|test|missile|launch|threat|escalat|doctrine|drill|mobiliz|explosion|blast|leak|meltdown|radiation|alert|emergency|shell|drone)"
                r"|\b(weapon|warhead|bomb|strike|attack|test|missile|launch|threat|escalat|doctrine|drill|mobiliz|explosion|blast|leak|meltdown|radiation|alert|emergency|shell|drone)\w*\b.{0,60}\bnuclear\b"),
    ("radiological", r"\bradiological|\bradiation (leak|release|alert)"),
    ("WMD", r"\bwmd\b|weapons? of mass destruction"),
    ("dirty bomb", r"dirty bomb"),
    ("DHS/NTAS bulletin", r"\bntas\b|national terrorism advisory|\bdhs\b.{0,40}\b(bulletin|advisory|alert)|\b(bulletin|advisory|alert)\b.{0,40}\bdhs\b"),
    ("attack on US soil", r"attacks? on (the )?(u\.?s\.?|american|united states|homeland)( soil| mainland| territory)|(u\.?s\.?|american|united states) (soil|homeland) (attack|strike)|attack(s|ed)? (in|on) the homeland|homeland attack|terror(ist)? attack in (the )?(u\.?s\.?|united states)"),
    ("Indiana/Midwest evacuation or shelter", r"(indiana|midwest|fort wayne|indianapolis|ohio|michigan|illinois|chicago|kentucky|wisconsin).{0,80}(evacuat|shelter[- ]in[- ]place|take shelter|shelter order)|(evacuat|shelter[- ]in[- ]place|take shelter|shelter order).{0,80}(indiana|midwest|fort wayne|indianapolis|ohio|michigan|illinois|chicago|kentucky|wisconsin)"),
]

STOP = set("the a an of to in on for and or at by with from as is are was were be been it its this that after over into new says say said".split())


def load_env(name):
    try:
        for line in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig"):
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return None


def canon_url(u):
    try:
        p = urlsplit(u.strip())
        host = p.netloc.lower()
        host = host[4:] if host.startswith("www.") else host
        q = [(k, v) for k, v in parse_qsl(p.query) if not k.lower().startswith(("utm_", "fbclid", "gclid", "cmp", "ocid", "ref", "taid"))]
        return urlunsplit((p.scheme.lower(), host, p.path.rstrip("/"), urlencode(q), ""))
    except Exception:
        return u.strip()


def tokens(t):
    return {w for w in re.findall(r"[a-z0-9]+", t.lower()) if w not in STOP and len(w) > 1}


def similar(a, b):
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= 0.7 or (min(len(ta), len(tb)) >= 5 and len(ta & tb) / min(len(ta), len(tb)) >= 0.9)


def domain_of(title):
    for n, pat in DOMAIN_RULES:
        if re.search(pat, title, re.I):
            return DOMAINS[n - 1]
    return DOMAINS[20]


def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\[\d+\]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*"})
    return urllib.request.urlopen(req, timeout=timeout).read()


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except Exception:
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone().replace(tzinfo=None)


def read_feed(name, url, cls):
    root = ET.fromstring(fetch(url))
    out = []
    for node in root.iter():
        tag = node.tag.split("}")[-1]
        if tag not in ("item", "entry"):
            continue
        kids = {}
        for c in node:
            kids.setdefault(c.tag.split("}")[-1], c)
        title = clean(kids["title"].text if "title" in kids else "")
        link = ""
        if "link" in kids:
            link = (kids["link"].text or "").strip() or kids["link"].attrib.get("href", "")
        if not link and "guid" in kids and (kids["guid"].text or "").startswith("http"):
            link = kids["guid"].text.strip()
        if not title or not link.startswith("http"):
            continue
        d = None
        for k in ("pubDate", "published", "updated", "date"):
            if k in kids:
                d = parse_date(kids[k].text)
                if d:
                    break
        src = name
        if "source" in kids and (kids["source"].text or "").strip():  # Google News carries the real outlet
            src = f"{kids['source'].text.strip()} via {name}"
            title = re.sub(r"\s+-\s+" + re.escape(kids["source"].text.strip()) + r"$", "", title)
        out.append({"title": title, "url": link, "source": src, "cls": cls, "pub": d})
    return out


# ---- Perplexity ------------------------------------------------------------------------------------------------
PPLX_Q = ("List the most important NEW world, US and public-safety news from the last 3 hours (include any report of chemical, "
          "biological, nuclear or radiological weapons or attacks, and any terror or emergency alert, even if disputed). "
          "Answer ONLY with lines in this exact form, one story per line, up to 10 lines, newest first:\n"
          "- [HH:MM UTC] [observed|claim] [official|press|solo|social] what happened in one plain sentence - source URL - money: none\n"
          "observed = a primary source said or did it; claim = asserted but unconfirmed. Every line needs a real source URL. "
          "No intro, no summary, no headings.")
LINE = re.compile(r"^-\s*\[[^\]]*\]\s*\[(observed|claim)\]\s*\[(official|press|solo|social)\]\s*(.+?)\s+[-\u2014\u2013]\s+(https?://\S+?)\s+[-\u2014\u2013]\s+money:", re.I)


def perplexity(state, force=False):
    """Returns (items, cost, note). Respects the monthly cap and the every-3-hours rule."""
    month = NOW.strftime("%Y-%m")
    spent = sum(c["cost"] for c in state.get("pplx", []) if c["ts"].startswith(month))
    if not force:
        if NOW.hour % 3 != 0:
            return [], 0.0, "Perplexity not due this hour"
        last = state.get("pplx", [])[-1:] or [{"ts": "2000-01-01T00:00"}]
        if datetime.fromisoformat(last[0]["ts"]) > NOW - timedelta(hours=2, minutes=30):
            return [], 0.0, "Perplexity already asked within 2.5 hours"
    if spent >= PPLX_MONTH_CAP:
        return [], 0.0, f"Perplexity monthly cap reached (${spent:.2f} of ${PPLX_MONTH_CAP:.2f}); skipped"
    k = load_env("PERPLEXITY_API_KEY")
    if not k:
        return [], 0.0, "PERPLEXITY_API_KEY missing"
    body = {"model": "sonar", "search_recency_filter": "day",
            "messages": [{"role": "system", "content": "You are a wire-service news desk. Follow the output format exactly."},
                         {"role": "user", "content": f"Now is {NOW.strftime('%Y-%m-%d %H:%M')} America/Indiana/Indianapolis. " + PPLX_Q}]}
    req = urllib.request.Request("https://api.perplexity.ai/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    cost = ((d.get("usage") or {}).get("cost") or {}).get("total_cost")
    if cost is None:
        cost = 0.008  # conservative estimate if the API omits it
    state.setdefault("pplx", []).append({"ts": NOW.strftime("%Y-%m-%dT%H:%M"), "cost": float(cost)})
    text = d["choices"][0]["message"]["content"]
    items = []
    for ln in text.splitlines():
        m = LINE.match(ln.strip())
        if m:
            items.append({"title": clean(m.group(3)), "url": m.group(4).rstrip(").,"), "source": "Perplexity (" + urlsplit(m.group(4)).netloc.replace("www.", "") + ")",
                          "cls": m.group(2).lower(), "label": m.group(1).lower(), "pub": None, "pplx": True})
    return items, float(cost), f"Perplexity asked: {len(items)} lines, ${cost:.4f}"


# ---- storage ---------------------------------------------------------------------------------------------------
def jl_path(day):
    return os.path.join(WIRE, f"{day}.jsonl")


def load_items(day):
    p = jl_path(day)
    out = []
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                try:
                    out.append(json.loads(ln))
                except ValueError:
                    pass
    return out


def render(day, items, notes, fails):
    by = {}
    for it in items:
        by.setdefault(it["domain"], []).append(it)
    n_src = len({i["source"] for i in items})
    out = [f"# wire capture — {day}",
           f"Writer: wire | Model: RSS/Atom + Perplexity Sonar, rolling (hourly feeds, Perplexity every 3h) | Time: {NOW.strftime('%H:%M')} (last update) | Window: whole local day, new stories only | Sources: {n_src} different outlets/feeds",
           "Status: " + ("substantive" if len(items) >= 12 else "thin" if items else "unavailable"),
           "Times below are when the wire FIRST SAW the story, not when it happened. Labels: press items are [claim] unless an official source; "
           "Perplexity lines keep Perplexity's own observed/claim label.", ""]
    for dom in DOMAINS:
        if dom in by:
            out.append(f"## {dom}")
            for it in sorted(by[dom], key=lambda x: x["seen"]):
                out.append(f"- [{it['seen']} local] [{it['label']}] [{it['cls']}] {it['title']} — {it['source']} — {it['url']} — money: none")
            out.append("")
    out += ["## Persistence", "Rolling wire: a story already in today's or yesterday's wire is not added again.", "",
            "## Silences", "Stories no feed or Perplexity question surfaced in the window do not appear here.", "",
            "## Could not see"]
    out += [f"- {f}" for f in fails] or ["- No feed failed on the last run."]
    out += [f"- {n}" for n in notes]
    return "\n".join(out) + "\n"


def safety_hits(title):
    return [lab for lab, pat in SAFETY if re.search(pat, title, re.I)]


def mailbox(to, subject, body):
    try:
        r = subprocess.run([sys.executable, MAILBOX, "send", "--from", "wire", "--to", to, "--subject", subject[:120], "--body", body],
                           capture_output=True, text=True, timeout=60)
        return r.returncode == 0
    except Exception:
        return False


def alert(new_items, send=True):
    cands = []
    for it in new_items:
        hits = safety_hits(it["title"])
        if not hits:
            continue
        pub = it.get("pub_dt")
        if pub and pub < NOW - timedelta(hours=ALERT_WINDOW_H):
            continue
        it["alert_hits"] = hits
        cands.append(it)
    sent = 0
    individual, rest = cands[:ALERT_MAX_INDIVIDUAL], cands[ALERT_MAX_INDIVIDUAL:]
    for it in individual:
        subj = f"WIRE: {', '.join(it['alert_hits'])} - {it['title'][:70]}"
        body = (f"Rolling wire item first seen {it['seen']} local, {DAY}. Matched: {', '.join(it['alert_hits'])}.\n"
                f"Headline: {it['title']}\nSource: {it['source']} ({it['cls']}, labelled {it['label']})\nLink: {it['url']}\n"
                f"File: watch/wire/{DAY}.md. Keyword match only: Satya decides the level; the wire has NOT touched the safety signal.")
        ok = (not send) or (mailbox("satya-twin", subj, body) & mailbox("claude", subj, body))
        it["alerted"] = bool(ok)
        sent += 1 if ok else 0
    if rest:
        body = "More wire items matched the safety words this run (individual-note limit reached). Nothing dropped:\n" + "\n".join(
            f"- [{i['seen']}] {', '.join(i['alert_hits'])}: {i['title']} — {i['source']} — {i['url']}" for i in rest)
        ok = (not send) or (mailbox("satya-twin", f"WIRE rollup: {len(rest)} more safety-word items", body) & mailbox("claude", f"WIRE rollup: {len(rest)} more safety-word items", body))
        for i in rest:
            i["alerted"] = bool(ok)
    return len(cands), sent


def git(*a):
    return subprocess.run(["git", *a], cwd=WATCH, capture_output=True, text=True, timeout=120)


def push(day):
    try:
        git("pull", "--rebase", "--autostash", "-q")
        git("add", "--", "wire")
        if git("diff", "--cached", "--quiet", "--", "wire").returncode != 0:
            git("commit", "-q", "-m", f"watch: wire {day} {NOW.strftime('%H:%M')}", "-m", "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>", "--", "wire")
            r = git("push", "-q")
            return "pushed" if r.returncode == 0 else "PUSH FAILED: " + r.stderr.strip()[:200]
        return "nothing new to commit"
    except Exception as e:
        return f"git error: {e}"


def main():
    args = set(sys.argv[1:])
    os.makedirs(WIRE, exist_ok=True)
    state = {}
    try:
        state = json.load(open(STATE, encoding="utf-8"))
    except Exception:
        pass
    today = load_items(DAY)
    known = today + load_items(YDAY)
    seen_urls = {canon_url(i["url"]) for i in known}
    titles = [i["title"] for i in known]
    first_run_today = not today

    cand, fails = [], []
    for name, url, cls in FEEDS:
        try:
            got = read_feed(name, url, cls)
        except Exception as e:
            fails.append(f"{name}: {str(e)[:80]}")
            continue
        recent = [g for g in got if g["pub"] is None or g["pub"] >= NOW - timedelta(hours=FEED_WINDOW_H)]
        recent.sort(key=lambda g: g["pub"] or NOW, reverse=True)
        for g in recent[:PER_FEED_CAP]:
            g["label"] = "observed" if cls == "official" else "claim"
            cand.append(g)

    notes, cost = [], 0.0
    if "--no-perplexity" not in args:
        try:
            pit, cost, note = perplexity(state, force="--force-perplexity" in args)
            cand += pit
            notes.append(note)
        except Exception as e:
            notes.append(f"Perplexity failed: {str(e)[:100]}")

    new = []
    for g in cand:
        cu = canon_url(g["url"])
        if cu in seen_urls or any(similar(g["title"], t) for t in titles):
            continue
        seen_urls.add(cu)
        titles.append(g["title"])
        it = {"seen": NOW.strftime("%H:%M"), "title": g["title"], "source": g["source"], "url": g["url"], "cls": g["cls"], "label": g["label"],
              "domain": domain_of(g["title"]), "pplx": bool(g.get("pplx")), "pub": g["pub"].isoformat(timespec="minutes") if g.get("pub") else None}
        it["pub_dt"] = g.get("pub")
        new.append(it)

    n_alert, n_sent = (0, 0)
    if new and "--no-alerts" not in args:
        n_alert, n_sent = alert(new)
    for it in new:
        it.pop("pub_dt", None)
        it.pop("alert_hits", None)

    all_today = today + new
    if new or not os.path.exists(os.path.join(WIRE, f"{DAY}.md")):
        with open(jl_path(DAY), "a", encoding="utf-8") as f:
            for it in new:
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
        open(os.path.join(WIRE, f"{DAY}.md"), "w", encoding="utf-8").write(render(DAY, all_today, notes, fails))
    state["pplx"] = [c for c in state.get("pplx", []) if c["ts"] >= (NOW - timedelta(days=62)).strftime("%Y-%m-%d")]
    json.dump(state, open(STATE, "w", encoding="utf-8"))

    try:   # must-cover list (11/6): always fresh next to the wire; the hourly push below carries it
        import build_top
        build_top.build(DAY)
    except Exception as e:
        notes.append(f"build_top failed (the 3:33 task retries): {e}")
    status = "no push" if "--no-push" in args else push(DAY)
    month_spend = sum(c["cost"] for c in state.get("pplx", []) if c["ts"].startswith(NOW.strftime("%Y-%m")))
    msg = (f"{NOW:%Y-%m-%d %H:%M} wire: {len(new)} new items (day total {len(all_today)}), feeds failed {len(fails)}/{len(FEEDS)}, "
           f"safety matches {n_alert} (notes sent {n_sent}), perplexity cost ${cost:.4f} (month ${month_spend:.3f}), {status}")
    print(msg)
    for f in fails:
        print("  feed fail:", f)
    for n in notes:
        print("  ", n)
    try:
        open(os.path.join(WATCH, "collectors", "wire_runs.log"), "a", encoding="utf-8").write(msg + "\n")
    except OSError:
        pass


if __name__ == "__main__":
    main()
