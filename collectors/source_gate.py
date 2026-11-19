"""source_gate.py - makes sure every news desk filed AND reached GitHub before the 3:45 cloud writer reads it (11/19/2026).

Why it exists (11/19): at 22:28 on 11/18 one git object in this repo came out corrupt. Every commit and push after that failed
silently (the desk scripts send git's output to Out-Null and the Windows tasks still report 0), so at 3:45 the cloud writer saw
NO desks, sent the "no show today" alarm, and the 4:20 MSI backup built the show alone. The same night the Claude desk wrote no
file at all (a stale DISABLED note in its instructions) and nobody saw it until 4:27.

Runs as Windows tasks "Watch Source Gate" (03:18 and 03:32) and "Watch Source Gate Final" (03:42, --final). Each run:
  1. Repo health: commit today's desk files that are on disk but not committed, and push anything GitHub doesn't have.
     A push that fails runs `git fsck` and mails Claude the error (Claude's mailbox waiter wakes it at any hour).
  2. Every desk due by now: the file must be on disk, big enough, and not a stub. Missing -> re-run that desk's own Windows
     task (schtasks /run: same environment as the nightly run; a task that is still running is left alone). At most
     2 re-runs per desk per day.
  3. Anything missing, re-run or failed -> one mailbox note to Claude with each desk's last log line, so the cause can be
     fixed in the moment. Final run only: buzz Jaron (ntfy) if a MUST desk is still missing, because the show goes out
     without it. MUST desks = Claude, Kimi, DeepSeek (Jaron's call, 11/19).
State: collectors/gate_state.json (re-runs per day). Log: collectors/gate_runs.log.
Usage: source_gate.py [--final] [--dry-run] [--day YYYY-MM-DD] [--now HH:MM]   (--day/--now only for testing, with --dry-run)
"""
import json, subprocess, sys, time
from functools import partial
from datetime import datetime, timedelta
from pathlib import Path

WATCH = Path(r"C:\Users\lilli\Projects\watch")
AI = Path(r"C:\Users\lilli\AI-Shared")
PY = r"C:\Users\lilli\scoop\apps\python312\current\python.exe"
STATE = WATCH / "collectors" / "gate_state.json"
LOG = WATCH / "collectors" / "gate_runs.log"
MAX_RERUNS = 2

# name, file, Windows task, due (HH:MM: when it is normally filed), min bytes, must-have, where its last log line lives
DESKS = [
    ("grok",       "grok/{d}.md",       "Watch Grok Meridian",    "02:05", 3000, False, "collectors/grok_runs.log"),
    ("msi",        "msi/{d}.md",        "Watch MSI Reader",       "03:06", 2000, False, None),
    ("perplexity", "perplexity/{d}.md", "Watch Perplexity Scout", "03:14", 2000, False, None),
    ("claude",     "claude/{d}.md",     "Watch Claude Desk",      "03:16", 3000, True,  r"C:\Users\lilli\AI-Shared\projects\news-show\runs.log"),
    ("kimi",       "kimi/{d}.md",       "Watch Kimi First Light", "03:16", 3000, True,  "collectors/kimi_runs.log"),
    ("codex",      "codex/{d}.md",      "Watch Codex Writer",     "03:17", 3000, False, "collectors/codex_runs.log"),
    ("deepseek",   "deepseek/{d}.md",   "Watch DeepSeek Reader",  "03:41", 3000, True,  "collectors/deepseek_runs.log"),
]
STUB_WORDS = ("no run took place", "did not run", "nothing to report today")
CORRUPT_WORDS = ("corrupt", "inflate", "unable to unpack", "bad object", "missing blob", "loose object")

args = sys.argv[1:]
FINAL, DRY = "--final" in args, "--dry-run" in args
def arg(flag):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else None
NOW = datetime.now()
if arg("--now"):
    h, m = map(int, arg("--now").split(":")); NOW = NOW.replace(hour=h, minute=m)
DAY = arg("--day") or NOW.strftime("%Y-%m-%d")
YDAY = (datetime.strptime(DAY, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
notes = []   # plain lines for the log and the mailbox
_run = partial(subprocess.run, creationflags=0x08000000)   # CREATE_NO_WINDOW: no console flashes from pythonw


def git(*a, timeout=180):
    """git in the watch repo; retries while another desk holds the index lock."""
    for i in range(6):
        r = _run(["git", *a], cwd=WATCH, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        if r.returncode == 0 or "index.lock" not in (r.stderr or ""):
            return r
        time.sleep(10)
    return r


def task_running(name):
    r = _run(["schtasks", "/query", "/tn", name, "/fo", "CSV", "/nh"], capture_output=True, text=True, errors="replace")
    return "Running" in r.stdout


def last_log_line(src, name):
    if not src:
        return ""
    p = Path(src) if Path(src).is_absolute() else WATCH / src
    try:
        lines = [l for l in p.read_text(encoding="utf-8", errors="replace").splitlines() if DAY in l]
    except OSError:
        return ""
    if name == "claude":
        lines = [l for l in lines if "claude desk capture" in l]
    return lines[-1][:240] if lines else ""


def desk_problem(rel, min_bytes):
    p = WATCH / rel
    if not p.exists():
        return "no file"
    size = p.stat().st_size
    if size < min_bytes:
        return f"only {size} bytes"
    # a real capture can quote these words in its header (11/17-18 Claude files do), so only a SMALL file counts as a stub
    if size < 5000 and any(w in p.read_text(encoding="utf-8", errors="replace").lower() for w in STUB_WORDS):
        return "stub (says it did not run)"
    return ""


def repo_health():
    """Commit desk + wire files that are on disk but not committed, then push whatever GitHub lacks."""
    paths = [f.format(d=DAY) for _, f, *_ in DESKS] + [f"grok/{DAY}-gaps.md"]
    paths += [f"wire/{d}{s}" for d in (DAY, YDAY) for s in (".md", "-top.md", ".jsonl")]
    paths = [p for p in paths if (WATCH / p).exists()]
    dirty = git("status", "--porcelain", "--", *paths).stdout.strip() if paths else ""
    if dirty and not DRY:
        a = git("add", "--", *paths)
        if a.returncode != 0:
            notes.append(f"REPO: git add failed: {a.stderr.strip()[:300]}")
        elif git("diff", "--cached", "--quiet").returncode != 0:
            c = git("commit", "-q", "-m", f"watch: source gate catch-up {DAY} {NOW:%H:%M}",
                    "-m", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
            if c.returncode != 0:
                notes.append(f"REPO: commit failed: {c.stderr.strip()[:300]}")
            else:
                notes.append(f"REPO: committed {len(dirty.splitlines())} desk/wire file(s) that were on disk but not in git")
    elif dirty:
        notes.append(f"REPO (dry run): would commit {len(dirty.splitlines())} file(s)")
    git("fetch", "-q", "origin", timeout=120)
    counts = git("rev-list", "--left-right", "--count", "HEAD...origin/master").stdout.split()
    ahead, behind = (int(counts[0]), int(counts[1])) if len(counts) == 2 else (0, 0)
    if behind and not DRY:
        pr = git("pull", "-q", "--rebase", "--autostash")
        if pr.returncode != 0:
            notes.append(f"REPO: pull failed: {pr.stderr.strip()[:300]}")
    if ahead and not DRY:
        p = git("push", "-q", "origin", "master")
        if p.returncode != 0:
            err = p.stderr.strip()
            notes.append(f"REPO: PUSH FAILED ({ahead} commit(s) stuck on the MSI): {err[:300]}")
            if any(w in err.lower() for w in CORRUPT_WORDS):
                fs = git("fsck", "--full", timeout=600)
                bad = "\n".join(l for l in (fs.stdout + fs.stderr).splitlines() if not l.startswith("dangling"))[:800]
                notes.append("REPO: git fsck says:\n" + (bad or "(nothing)"))
        else:
            notes.append(f"REPO: pushed {ahead} commit(s) that were stuck on the MSI")
    elif ahead:
        notes.append(f"REPO (dry run): {ahead} commit(s) not on GitHub")


def main():
    state = {}
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    reruns = state.setdefault(DAY, {})
    for k in [k for k in state if k < YDAY]:
        state.pop(k)

    repo_health()
    hhmm = NOW.strftime("%H:%M")
    missing_must, reran = [], []
    for name, f, task, due, min_b, must, logsrc in DESKS:
        if hhmm < due:
            continue
        prob = desk_problem(f.format(d=DAY), min_b)
        if not prob:
            continue
        why = last_log_line(logsrc, name)
        line = f"{name.upper()}{' (MUST)' if must else ''}: {prob}" + (f" | last log: {why}" if why else "")
        if task_running(task):
            notes.append(line + " | its task is still running, left alone")
        elif reruns.get(name, 0) >= MAX_RERUNS:
            notes.append(line + f" | already re-run {MAX_RERUNS}x today, not again")
        elif DRY:
            notes.append(line + f" | (dry run) would re-run '{task}'")
        else:
            r = _run(["schtasks", "/run", "/tn", task], capture_output=True, text=True, errors="replace")
            reruns[name] = reruns.get(name, 0) + 1
            reran.append(name)
            notes.append(line + (f" | re-ran '{task}' (try {reruns[name]})" if r.returncode == 0 else f" | re-run FAILED: {r.stderr.strip()[:150]}"))
        if must:
            missing_must.append(name)

    # final run: give a quick re-run (DeepSeek takes under a minute) a chance to land, then push again
    if FINAL and reran and not DRY:
        for _ in range(12):
            time.sleep(10)
            if all(not desk_problem(f.format(d=DAY), mb) for n, f, _, _, mb, _, _ in DESKS if n in reran):
                break
        still = [n for n, f, _, _, mb, _, _ in DESKS if n in reran and desk_problem(f.format(d=DAY), mb)]
        landed = [n for n in reran if n not in still]
        if landed:
            notes.append("LANDED after re-run: " + ", ".join(landed))
            missing_must = [n for n in missing_must if n not in landed]
            repo_health()

    if not DRY:
        STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")
    tag = "final" if FINAL else "check"
    summary = f"{NOW:%Y-%m-%d %H:%M} | gate {tag}{' (dry run)' if DRY else ''} | " + (" || ".join(n.replace("\n", " / ") for n in notes) if notes else "all desks due by now are filed and on GitHub")
    if not DRY:
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(summary + "\n")
    print(summary)
    if notes and not DRY:
        body = (f"Source gate {tag} run, {NOW:%H:%M} {DAY}. The cloud writer reads the watch repo at 3:45; the MSI backup writer runs at 4:20.\n\n"
                + "\n".join("- " + n for n in notes)
                + "\n\nFix what you can now (cause of a missing desk, a stuck push), then re-run the desk's task. Log: Projects/watch/collectors/gate_runs.log")
        _run([PY, str(AI / "tools" / "mailbox.py"), "send", "--from", "source-gate", "--to", "claude",
                        "--subject", f"Source gate {tag}: " + ("MUST desk missing: " + ", ".join(missing_must) if missing_must else "fixed or flagged something"),
                        "--body", body], capture_output=True, timeout=60)
    if FINAL and missing_must and not DRY:
        names = ", ".join(n.capitalize() for n in missing_must)
        _run([PY, str(AI / "tools" / "ntfy-say.py"), "News sources",
                        f"Heads up: {names} did not file for today's show, so it goes out without {'it' if len(missing_must) == 1 else 'them'}. Claude has the details and is on it."],
                       capture_output=True, timeout=60)


if __name__ == "__main__":
    main()
