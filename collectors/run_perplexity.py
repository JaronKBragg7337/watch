"""Perplexity capture for the daily watch (added 2026-11-05 after a spot-check: Perplexity's Discover page had 4 stories the
news team missed, including the NYT Iran chemical-weapons report two days running).

Registered as Windows task "Watch Perplexity Scout", daily 03:10 local, so the 3:35 blind-spot check and the 3:45 / 4:20 writers
can read it. Uses the Perplexity API (Sonar, live web search with sources). Cost is about half a cent per question; 5 questions
a day is roughly $0.75 a month. Key: PERPLEXITY_API_KEY in ~/.secrets/keys.env (never printed).

Writes perplexity/YYYY-MM-DD.md in FORMAT.md style and pushes it to the watch repo.
"""
import json, os, subprocess, sys, urllib.request
from datetime import datetime

WATCH = r"C:\Users\lilli\Projects\watch"
DAY = datetime.now().strftime("%Y-%m-%d")
NOW = datetime.now().strftime("%H:%M")

# One question per area; each answer must be FORMAT.md item lines with a source URL.
DESKS = [
    ("05 geopolitics / conflict / borders / law", "the biggest world news: wars, strikes, ceasefires, diplomacy, sanctions, "
     "and ANY report about weapons of mass destruction (chemical, biological, nuclear), even if disputed"),
    ("13 U.S. politics and elections", "US politics, Congress, the White House, courts and elections"),
    ("02 stocks / macro / rates / labor", "markets, central banks, interest rates, inflation, energy prices and big company news"),
    ("03 AI / models / infra / pricing of intelligence", "AI, tech, cyberattacks, outages and science or space news"),
    ("21 uncategorised", "anything else major from Asia, Africa, Latin America, Europe or the Middle East that a US outlet might skip"),
]

RULES = ("Answer ONLY with lines in this exact form, one story per line, 4 to 8 lines, newest and most important first:\n"
         "- [HH:MM local or day] [observed|claim] [official|press|solo|social] what happened in one plain sentence - source URL - money: none\n"
         "observed = a primary source said or did it; claim = asserted but not confirmed (mark disputed reports as claim). "
         "Every line needs a real source URL from your search. No intro, no summary, no markdown headings.")


def key():
    for line in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig"):
        if line.startswith("PERPLEXITY_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"')
    sys.exit("PERPLEXITY_API_KEY missing")


def ask(k, topic):
    body = {"model": "sonar", "search_recency_filter": "day",
            "messages": [{"role": "system", "content": RULES},
                         {"role": "user", "content": f"Today is {DAY}. List the most important news from the last 24 hours about {topic}."}]}
    req = urllib.request.Request("https://api.perplexity.ai/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + k, "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=120))
    text = d["choices"][0]["message"]["content"].strip()
    cost = ((d.get("usage") or {}).get("cost") or {}).get("total_cost", 0)
    return [l for l in text.splitlines() if l.strip().startswith("- ")], d.get("citations") or [], cost


def main():
    k = key()
    out = [f"# perplexity capture — {DAY}",
           f"Writer: perplexity | Model: sonar (Perplexity API, live web search) | Time: {NOW}",
           "Window: last 24h | Sources: web (each line cites its own source)",
           "Status: substantive", ""]
    total, fails = 0.0, []
    for head, topic in DESKS:
        out.append(f"## {head}")
        try:
            lines, cites, cost = ask(k, topic)
            total += cost
            out += lines or ["- (no lines returned)"]
            if cites:
                out.append("  sources searched: " + " ".join(cites[:8]))
        except Exception as e:  # one desk failing must not lose the others
            fails.append(f"{head}: {e}")
            out.append("- (this desk failed; see Could not see)")
        out.append("")
    out += ["## Could not see"] + ([f"- {f}" for f in fails] or ["- Nothing failed."]) + ["", f"Cost today: ${total:.4f}"]
    if len(fails) == len(DESKS):
        out[4] = "Status: unavailable"
    os.makedirs(os.path.join(WATCH, "perplexity"), exist_ok=True)
    path = os.path.join(WATCH, "perplexity", f"{DAY}.md")
    open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"wrote perplexity/{DAY}.md, cost ${total:.4f}, failed desks {len(fails)}")
    os.chdir(WATCH)
    subprocess.run(["git", "pull", "--rebase", "--autostash", "-q"])
    subprocess.run(["git", "add", "--", f"perplexity/{DAY}.md"])
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
        subprocess.run(["git", "commit", "-q", "-m", f"watch: perplexity {DAY}", "-m", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"])
        subprocess.run(["git", "push", "-q"])


if __name__ == "__main__":
    main()
