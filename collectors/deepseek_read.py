"""DeepSeek as the Eastern READER (its API has no web access): reads today's captures from every collector and writes
deepseek/YYYY-MM-DD.md in the shared format, plus Convergence / Divergence / From the other hemisphere.
Run daily on the MSI after the collectors:  python collectors/deepseek_read.py [YYYY-MM-DD]
Uses DEEPSEEK_API_KEY from ~/.secrets/keys.env. (Claude Code, 2026-09-18)"""
from __future__ import annotations
import json, sys, urllib.request
from common import ROOT, today, keys, captures_for

day = sys.argv[1] if len(sys.argv) > 1 else today().strftime("%Y-%m-%d")
out = ROOT / "deepseek" / f"{day}.md"
caps = [(w, t) for w, t in captures_for(day) if w != "deepseek"]
now = today().strftime("%H:%M")
if not caps:
    out.write_text(f"# deepseek capture — {day}\nWriter: deepseek | Model: deepseek-chat | Time: {now}\n"
                   f"Window: reader | Sources: other captures (reader)\nStatus: unavailable\n\n## Could not see\n"
                   f"No captures from any collector for {day} at run time.\n", encoding="utf-8")
    print("no captures yet; wrote unavailable"); sys.exit(0)
fmt = (ROOT / "FORMAT.md").read_text(encoding="utf-8")
corpus = "\n\n".join(f"===== CAPTURE FROM {w} =====\n{t}" for w, t in caps)
writers = ", ".join(w for w, _ in caps)
prompt = (
    "You are the reader for a daily watch. You have NO web access; you read only the captures below, written today by other AIs "
    "that do have the web. Write ONE capture in exactly the format described: headings 01-11, then Persistence, Silences, Could not "
    "see, then the reader sections Convergence, Divergence, From the other hemisphere. Keep every item labelled observed / claim / "
    "theory and keep its source URL and money tag from the capture you took it from. Do not drop an item because it is unofficial or "
    "speculative; label it. Say plainly what you could not assess.\n"
    f"Header: Writer: deepseek | Model: deepseek-chat | Time: {now} | Window: reader | Sources: other captures (reader) | "
    "Status: substantive or thin.\n\nFORMAT:\n" + fmt + f"\n\nTODAY'S CAPTURES ({len(caps)} writers: {writers}):\n" + corpus)
body = {"model": "deepseek-chat", "temperature": 0.2, "messages": [{"role": "user", "content": prompt}]}
req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json", "Authorization": "Bearer " + keys()["DEEPSEEK_API_KEY"]})
with urllib.request.urlopen(req, timeout=300) as r:
    text = json.load(r)["choices"][0]["message"]["content"]
if not text.lstrip().startswith("#"):
    text = f"# deepseek capture — {day}\n" + text
out.write_text(text.strip() + "\n", encoding="utf-8")
print(f"wrote {out} ({len(text)} chars) from {len(caps)} captures: {writers}")
