"""first_light_adds.py - what did First Light (kimi/) add that no other desk had? (2026-10-10, Claude Code)
Vex's challenge: more Eastern sources != more independence; models can echo the same wires. So each day we count the source
domains and URLs in kimi/D.md that appear in NO other capture that day, and append one line to collectors/first_light_adds.log.
Later checking (did those items hold up?) builds on this log.   python collectors/first_light_adds.py [YYYY-MM-DD]
"""
import glob, os, re, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
day = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
url_re = re.compile(r"https?://[^\s)>\]]+")
dom = lambda u: re.sub(r"^www\.", "", u.split("/")[2].lower())
k = os.path.join(ROOT, "kimi", f"{day}.md")
if not os.path.exists(k):
    sys.exit(f"no kimi/{day}.md")
kim = set(url_re.findall(open(k, encoding="utf-8", errors="ignore").read()))
others = set()
for f in glob.glob(os.path.join(ROOT, "*", f"{day}.md")):
    if os.sep + "kimi" + os.sep not in f:
        others |= set(url_re.findall(open(f, encoding="utf-8", errors="ignore").read()))
od = {dom(u) for u in others}
new_dom = sorted({dom(u) for u in kim} - od)
line = f"{day} | kimi urls {len(kim)} | not in any other desk: urls {len(kim - others)}, domains {len(new_dom)} | {', '.join(new_dom[:25])}"
print(line)
open(os.path.join(ROOT, "collectors", "first_light_adds.log"), "a", encoding="utf-8").write(line + "\n")
