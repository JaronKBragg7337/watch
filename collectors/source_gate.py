"""source_gate.py - makes sure every news desk filed AND reached GitHub before the 3:45 cloud writer reads it (11/19/2026).

Why it exists (11/19): at 22:28 on 11/18 one git object in this repo came out corrupt. Every commit and push after that failed
silently (the desk scripts send git's output to Out-Null and the Windows tasks still report 0), so at 3:45 the cloud writer saw
NO desks, sent the "no show today" alarm, and the 4:20 MSI backup built the show alone. The same night the Claude desk wrote no
file at all (a stale DISABLED note in its instructions) and nobody saw it until 4:27. Kimi had also filed nothing on 11/17-18.

Runs as Windows tasks "Watch Source Gate" (03:18, 03:32) and "Watch Source Gate Final" (03:42, --final). Triggers keep LOCAL
time (no fixed UTC offset), so daylight saving can't push the gate past the 3:45 writer. Each run, in this order:
  1. Local commit (no network): desk + wire files on disk but not committed get committed, except a desk still writing.
  2. Desks due by now: file on disk, big enough, not a stub, header not "Status: unavailable". Missing -> re-run that desk's
     own Windows task (schtasks /run: same environment as the nightly run). A task still running is left alone (the final run
     waits for it until about 3:44:30). At most 2 re-runs per desk per day.
  3. Network: fetch, push anything GitHub lacks, then confirm each desk file is really on origin/master. Every git result is
     checked; a corrupt-looking error runs `git fsck` once. Git calls time out instead of hanging, and never crash the gate.
  4. Anything wrong -> one mailbox note to Claude (its waiter wakes it at any hour) with each desk's last log line. If the
     mailbox can't be reached, the note goes to Jaron's phone instead. Final run only: buzz Jaron if a MUST desk (Claude, Kimi,
     DeepSeek - his call, 11/19) is still missing, because the show goes out without it. Routine things only go to the log.
State: collectors/gate_state.json (re-runs per day). Log: collectors/gate_runs.log.
Usage: source_gate.py [--final] [--dry-run] [--manual] [--day YYYY-MM-DD] [--now HH:MM]
       --manual = run by hand (skips the "fired at the wrong hour" check); --day/--now only for testing, with --dry-run.
"""
import json, os, re, subprocess, sys, time, traceback
from datetime import datetime, timedelta
from functools import partial
from pathlib import Path

WATCH = Path(r"C:\Users\lilli\Projects\watch")
AI = Path(r"C:\Users\lilli\AI-Shared")
PY = r"C:\Users\lilli\scoop\apps\python312\current\python.exe"
STATE = WATCH / "collectors" / "gate_state.json"
LOG = WATCH / "collectors" / "gate_runs.log"
MAX_RERUNS = 2
NOWIN = 0x08000000   # CREATE_NO_WINDOW: no console flashes from pythonw
_run = partial(subprocess.run, creationflags=NOWIN)
# git gives up on a stalled connection by itself (under 30 s below 1 KB/s) and never waits for a login prompt
GIT_ENV = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never", GIT_HTTP_LOW_SPEED_LIMIT="1000", GIT_HTTP_LOW_SPEED_TIME="30")

# name, file, Windows task, due (HH:MM: normally filed by), min bytes, must-have, where its last log line lives
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
STATUS_RE = re.compile(r"(?i)\bStatus:\s*([a-z]+)")   # FORMAT.md header: "Status: substantive | thin | unavailable"
CORRUPT_WORDS = ("corrupt", "inflate", "unable to unpack", "bad object", "missing blob", "loose object")

args = sys.argv[1:]
FINAL, DRY, MANUAL = "--final" in args, "--dry-run" in args, "--manual" in args
def arg(flag):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else None
NOW = datetime.now()
if arg("--now"):
    h, m = map(int, arg("--now").split(":")); NOW = NOW.replace(hour=h, minute=m)
TESTING = bool(arg("--now") or arg("--day"))
DAY = arg("--day") or NOW.strftime("%Y-%m-%d")
YDAY = (datetime.strptime(DAY, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
notes = []   # worth telling Claude
quiet = []   # normal-night details: log only
_fsck_done = []


def git(*a, timeout=180):
    """git in the watch repo. Retries while another desk holds the index lock. Never raises: a timeout or a git that
    won't start comes back as a failed result (124 / 127), and a timed-out git is killed with its helpers."""
    r = None
    for _ in range(6):
        try:
            p = subprocess.Popen(["git", *a], cwd=WATCH, env=GIT_ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 text=True, encoding="utf-8", errors="replace", creationflags=NOWIN)
        except OSError as e:
            return subprocess.CompletedProcess(a, 127, "", f"git could not start: {e}")
        try:
            out, err = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            _run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)   # only this git and its own children
            try:
                p.communicate(timeout=15)
            except Exception:
                pass
            return subprocess.CompletedProcess(a, 124, "", f"git {a[0]} timed out after {timeout}s")
        r = subprocess.CompletedProcess(a, p.returncode, out or "", err or "")
        if r.returncode == 0 or "index.lock" not in r.stderr:
            return r
        time.sleep(10)
    return r


def repo_fail(step, r):
    err = (r.stderr + " " + r.stdout).strip()
    notes.append(f"REPO: git {step} failed (exit {r.returncode}): {err[:300]}")
    if not _fsck_done and any(w in err.lower() for w in CORRUPT_WORDS):
        _fsck_done.append(1)
        fs = git("fsck", "--full", timeout=600)
        bad = "\n".join(l for l in (fs.stdout + fs.stderr).splitlines() if not l.startswith("dangling"))[:800]
        notes.append("REPO: git fsck says:\n" + (bad or "(nothing)"))


def task_running(name):
    try:
        r = _run(["schtasks", "/query", "/tn", name, "/fo", "CSV", "/nh"], capture_output=True, text=True, errors="replace", timeout=30)
        return "Running" in r.stdout
    except Exception:
        return False


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
    text = p.read_text(encoding="utf-8", errors="replace")
    m = STATUS_RE.search("\n".join(text.splitlines()[:12]))
    if m and m.group(1).lower() == "unavailable":   # the template line itself reads "substantive | ..." and is not flagged
        return 'header says "Status: unavailable"'
    # a real capture can quote these words in its header (11/17-18 Claude files do), so only a SMALL file counts as a stub
    if size < 5000 and any(w in text.lower() for w in STUB_WORDS):
        return "stub (says it did not run)"
    return ""


def local_commit(writing):
    """Commit desk + wire files that are on disk but not in git. Skips desks whose task is still writing."""
    desk_paths = [f.format(d=DAY) for n, f, *_ in DESKS if n not in writing] + [f"grok/{DAY}-gaps.md"]
    wire_paths = [f"wire/{d}{s}" for d in (DAY, YDAY) for s in (".md", "-top.md", ".jsonl")]
    paths = [p for p in desk_paths + wire_paths if (WATCH / p).exists()]
    if not paths:
        return
    st = git("status", "--porcelain", "--", *paths)
    if st.returncode != 0:
        return repo_fail("status", st)
    dirty = [l[3:].strip() for l in st.stdout.splitlines() if l.strip()]
    if not dirty:
        return
    desks_dirty = [d for d in dirty if not d.startswith("wire/")]
    if DRY:
        return notes.append(f"REPO (dry run): would commit {', '.join(dirty)}")
    a = git("add", "--", *paths)
    if a.returncode != 0:
        return repo_fail("add", a)
    if git("diff", "--cached", "--quiet").returncode == 0:
        return
    c = git("commit", "-q", "-m", f"watch: source gate catch-up {DAY} {NOW:%H:%M}", "-m", "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    if c.returncode != 0:
        return repo_fail("commit", c)
    # a desk file its own script didn't commit means that script's git failed: worth knowing. Wire leftovers are routine.
    (notes if desks_dirty else quiet).append(f"REPO: committed {', '.join(dirty)} (on disk but not in git)")


def network():
    """Fetch, push what GitHub lacks, then check each desk file is on origin/master. Returns False if GitHub couldn't be checked."""
    f = git("fetch", "-q", "origin", timeout=120)
    if f.returncode != 0:
        repo_fail("fetch", f)
        return False
    rl = git("rev-list", "--left-right", "--count", "HEAD...origin/master")
    if rl.returncode != 0 or len(rl.stdout.split()) != 2:
        repo_fail("rev-list", rl)
        return False
    ahead, behind = map(int, rl.stdout.split())
    if DRY:
        if ahead or behind:
            notes.append(f"REPO (dry run): {ahead} commit(s) not on GitHub, {behind} not here")
    else:
        if behind:
            pr = git("pull", "-q", "--rebase", "--autostash")
            if pr.returncode != 0:
                repo_fail("pull --rebase", pr)
                git("rebase", "--abort")   # never leave the desks a half-done rebase
        if ahead:
            p = git("push", "-q", "origin", "HEAD:master")
            if p.returncode != 0:
                repo_fail(f"push ({ahead} commit(s) stuck on the MSI)", p)
            else:
                notes.append(f"REPO: pushed {ahead} commit(s) that were stuck on the MSI (a desk's own push didn't go through)")
                git("fetch", "-q", "origin", timeout=120)
    missing = []
    for name, f, *_ in DESKS:
        rel = f.format(d=DAY)
        if (WATCH / rel).exists():
            ls = git("ls-tree", "--name-only", "origin/master", "--", rel)
            if ls.returncode != 0 or rel not in ls.stdout:
                missing.append(name)
    if missing:
        notes.append("NOT ON GITHUB (on the MSI only, so the 3:45 cloud writer can't see them): " + ", ".join(missing))
    return True


def main():
    state = {}
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    reruns = state.setdefault(DAY, {})
    for k in [k for k in state if k < YDAY]:
        state.pop(k)
    missing_must, reran, waiting = [], [], []
    try:
        if not (DRY or MANUAL or TESTING) and NOW.hour != 3:
            notes.append(f"GATE fired at {NOW:%H:%M}, not in the 3 AM hour: its trigger time has drifted (check the task's StartBoundary)")
        hhmm = NOW.strftime("%H:%M")
        due = [d for d in DESKS if hhmm >= d[3]]
        writing = {d[0] for d in due if task_running(d[2])}
        local_commit(writing)
        for name, f, task, _due, min_b, must, logsrc in due:
            prob = desk_problem(f.format(d=DAY), min_b)
            if not prob:
                continue
            why = last_log_line(logsrc, name)
            line = f"{name.upper()}{' (MUST)' if must else ''}: {prob}" + (f" | last log: {why}" if why else "")
            if name in writing:
                if FINAL:
                    waiting.append(name); notes.append(line + " | still running, waiting for it")
                    if must:
                        missing_must.append(name)
                else:
                    quiet.append(line + " | still running, left alone")
                continue
            if reruns.get(name, 0) >= MAX_RERUNS:
                notes.append(line + f" | already re-run {MAX_RERUNS}x today, not again")
            elif DRY:
                notes.append(line + f" | (dry run) would re-run '{task}'")
            else:
                r = _run(["schtasks", "/run", "/tn", task], capture_output=True, text=True, errors="replace", timeout=60)
                reruns[name] = reruns.get(name, 0) + 1
                if r.returncode == 0:
                    reran.append(name); notes.append(line + f" | re-ran '{task}' (try {reruns[name]})")
                else:
                    notes.append(line + f" | re-run FAILED to start: {(r.stderr or r.stdout).strip()[:150]}")
            if must:
                missing_must.append(name)

        # final run: give re-runs and still-running desks until about 3:44:30 to land (the cloud writer clones at ~3:45:40)
        waitfor = reran + waiting
        if FINAL and waitfor and not DRY:
            end = datetime.now().replace(hour=3, minute=44, second=30) if datetime.now().hour == 3 else datetime.now() + timedelta(minutes=2)
            spec = {n: (f, mb) for n, f, _, _, mb, _, _ in DESKS}
            pending = list(waitfor)
            while pending and datetime.now() < end:
                time.sleep(10)
                pending = [n for n in pending if desk_problem(spec[n][0].format(d=DAY), spec[n][1])]
            landed = [n for n in waitfor if n not in pending]
            if landed:
                notes.append("LANDED in time: " + ", ".join(landed))
                missing_must = [n for n in missing_must if n not in landed]
                local_commit(set())
        network()
    except Exception:
        notes.append("GATE CRASHED (the checks above may be incomplete):\n" + traceback.format_exc()[-900:])
    finally:
        if not DRY:
            try:
                STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")
            except OSError:
                pass
        tag = "final" if FINAL else "check"
        parts = notes + [q + " [log only]" for q in quiet]
        summary = f"{NOW:%Y-%m-%d %H:%M} | gate {tag}{' (dry run)' if DRY else ''} | " + (" || ".join(p.replace("\n", " / ") for p in parts) if parts else "all desks due by now are filed and on GitHub")
        if not DRY:
            try:
                with LOG.open("a", encoding="utf-8") as fh:
                    fh.write(summary + "\n")
            except OSError:
                pass
        print(summary)
        if notes and not DRY:
            subject = f"Source gate {tag}: " + ("MUST desk missing: " + ", ".join(missing_must) if missing_must else "fixed or flagged something")
            body = (f"Source gate {tag} run, {NOW:%H:%M} {DAY}. The cloud writer reads the watch repo at 3:45; the MSI backup writer runs at 4:20.\n\n"
                    + "\n".join("- " + n for n in notes)
                    + "\n\nFix what you can now (cause of a missing desk, a stuck push), then re-run the desk's task. Log: Projects/watch/collectors/gate_runs.log")
            sent = False
            try:
                m = _run([PY, str(AI / "tools" / "mailbox.py"), "send", "--from", "source-gate", "--to", "claude", "--subject", subject, "--body", body],
                         capture_output=True, text=True, errors="replace", timeout=60)
                sent = m.returncode == 0
            except Exception:
                pass
            if not sent:   # nobody would hear it otherwise
                try:
                    _run([PY, str(AI / "tools" / "ntfy-say.py"), "News sources", f"The news source check couldn't reach Claude's mailbox. {subject}. {notes[0][:160]}"], capture_output=True, timeout=60)
                except Exception:
                    pass
        if FINAL and missing_must and not DRY:
            names = ", ".join(n.capitalize() for n in missing_must)
            try:
                _run([PY, str(AI / "tools" / "ntfy-say.py"), "News sources",
                      f"Heads up: {names} didn't file in time for today's 3:45 show, so it goes out without {'it' if len(missing_must) == 1 else 'them'}. Claude has the details."],
                     capture_output=True, timeout=60)
            except Exception:
                pass


if __name__ == "__main__":
    main()
