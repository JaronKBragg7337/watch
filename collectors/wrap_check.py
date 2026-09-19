"""The wrapping check - did the organizer transfer at the temperature it received? (Claude Code, 2026-09-19; Jaron's research/WORD-WRAPPING.md)
usage: python collectors/wrap_check.py [YYYY-MM-DD]
Reads today's captures and today's brief + market feed. Counts: hedges the brief added that no capture used; market-feed lines whose
label or source is not found in any capture; capture items with a money tag that never reached the feed. Writes brief/wrap_YYYY-MM-DD.json.
It measures words, not truth. A high count means the seat changed the temperature; it does not say who is right."""
from __future__ import annotations
import json, re, sys
from common import ROOT, today, captures_for

HEDGES = ["may not", "might not", "could argue", "doesn't necessarily", "does not necessarily", "some suggest", "some would say",
          "it is worth noting", "it's worth noting", "arguably", "to be fair", "in fairness", "not necessarily", "could be seen as",
          "one could", "it should be noted", "importantly,", "reassuringly", "no cause for", "there is no need to"]
day = sys.argv[1] if len(sys.argv) > 1 else today().strftime("%Y-%m-%d")
caps = captures_for(day)
brief_p, feed_p = ROOT / "brief" / f"{day}.md", ROOT / "market-feed" / f"{day}.jsonl"
if not caps or not brief_p.exists():
    print("nothing to check (need captures and a brief for", day, ")"); sys.exit(0)
corpus = "\n".join(t for _, t in caps).lower(); brief = brief_p.read_text(encoding="utf-8"); bl = brief.lower()
cap_urls = set(re.findall(r"https?://\S+", corpus)); cap_money = [ln for _, t in caps for ln in t.splitlines() if "money:" in ln and "money: none" not in ln]
hedges_added = {h: bl.count(h) - corpus.count(h) for h in HEDGES if bl.count(h) > corpus.count(h)}
feed = [json.loads(l) for l in feed_p.read_text(encoding="utf-8").splitlines() if l.strip()] if feed_p.exists() else []
feed_bad_source = [f for f in feed if f.get("source", "").lower() not in cap_urls]
feed_bad_label = [f for f in feed if f.get("label") not in ("observed", "claim", "theory")]
feed_srcs = {f.get("source", "").lower() for f in feed}
money_not_fed = [ln for ln in cap_money if not any(u in ln.lower() for u in feed_srcs)]
out = {"day": day, "writers": [w for w, _ in caps], "hedges_added": hedges_added, "feed_lines": len(feed), "feed_source_not_in_captures": len(feed_bad_source),
       "feed_bad_label": len(feed_bad_label), "capture_money_items": len(cap_money), "money_items_not_in_feed": len(money_not_fed),
       "wrap_score": sum(hedges_added.values()) + len(feed_bad_source) + len(feed_bad_label)}
(ROOT / "brief" / f"wrap_{day}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out))
