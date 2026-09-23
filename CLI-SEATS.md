CLI seats on the MSI - which AI can be run headless from Jaron's machine, on which meter, and how.
Written 2026-09-21 by Claude Code with Jaron. Plain words. Every AI in the system should read this once; it changes how the
writers run. Grok bots (Elons Twin, Live Wire, Bridge, Scout): this is why nobody has to carry task text between apps anymore.

THE SHORT VERSION

Three AIs can be started from a command line on the MSI and each one bills a different pool. None of them touch Live Wire's pool.
  Codex CLI   (codex exec)   - ChatGPT subscription, model Luna (gpt-5.6-luna). Jaron: cheap enough to run 24/7 and never hit usage.
  Grok Build  (grok -p ...)  - SuperGrok / grok.com subscription, model grok-4.7. Separate meter from the Grok bots' meter.
                               On 2026-09-21 the bots' meter was at 89% and this one at 3%. Signed in as acsassociation7337@gmail.com.
  DeepSeek    (python)       - API credits, pennies per run. No web; it reads the captures, it does not search.
Claude Code's own daily writer (watch-collect) exists but is paused for usage until the reset on Wednesday 2026-09-23, about 4 PM ET.
Note 2026-09-22: Opus 5.5 shipped, claimed at Fable 5.1 level for most tasks and 40% cheaper to run than Opus 5. The MSI's CLI
was updated to 2.1.280 so it is selectable. When the writer comes back it should run on 5.5, not 5, for the same reason Codex
runs on Luna: the cheap seat is the one that gets to run every day.
Astra (ChatGPT's best model) is reserved for fly-brain work when that resumes; not for daily writers.

WHAT RUNS ON A SCHEDULE (Windows Task Scheduler on the MSI, America/Indiana/Indianapolis)
  07:30  Watch Codex Writer     collectors/run_codex.ps1    -> codex/YYYY-MM-DD.md   (first run 2026-09-21: 21 domains, 46 sources)
  08:00  Watch Grok Writer      collectors/run_grok.ps1     -> grok/YYYY-MM-DD.md    (registered 2026-09-21 after the first by-hand run)
  09:00  Watch DeepSeek Reader  collectors/run_deepseek.ps1 -> deepseek/YYYY-MM-DD.md
  11:00  Organizer seat         brief/TASK.txt              -> brief/ + market-feed/  (Elons Twin has been sitting it by hand)
Each runner pulls, runs the AI, commits "watch: <writer> YYYY-MM-DD", pushes. Run logs: collectors/<writer>_runs.log.

HOW TO CALL EACH ONE (for any AI or person on the MSI)
  Codex:  put the prompt in a file, then   codex --search exec -s workspace-write --skip-git-repo-check -C <repo> - < prompt.txt
          --search goes BEFORE exec. A multi-line prompt on the command line is parsed as a command; use stdin or a file.
          Read-only review of another AI's work:   codex exec -s read-only --skip-git-repo-check -C <repo> "<one-line prompt>"
  Grok:   grok --prompt-file prompt.txt --always-approve --max-turns 80 --no-memory --no-subagents --no-plan --cwd <repo>
          Without --always-approve a headless run plans one turn and exits with nothing written. Web search and X are on by default.
          Login: grok login --device-code  prints a URL and code; Jaron confirms on his phone. Tokens expire; if a run says
          "Not signed in", that is the fix, and only Jaron does it.
  DeepSeek:  python collectors/deepseek_read.py  (key in the MSI env; never in this repo)
  Claude Code:  the watch-collect scheduled task in Jaron's Claude app; paused.
  Local Qwen:   python C:\Users\lilli\AI-Shared\tools\qwen-bridge.py "<question>"  - free, local, no web, no money.

WHAT THIS CHANGES FOR THE GROK BOTS
  Bridge no longer needs to run grok/TASK.txt; the MSI runs it at 08:00 on the SuperGrok meter. Bridge's and Scout's task texts
  are kept under agents/grok-bots/ so nothing is lost. Elons Twin still sits the organizer seat until that is scheduled too.
  Live Wire's pool is untouched by any of this; that was the rule and it still holds.

ALSO ON THE MACHINE, NOT WIRED YET
  Kimi Desktop - Kimi's own agent runtime with a local gateway (port 18679 when the app is open), built-in skills, and a job
  store. Jaron: "it's definitely its own thing." To be tested as a fourth writer when the app is open. Its plan, not Jaron's.

ONE LINE THE CLAUDE SEAT DRAWS FOR ITSELF (2026-09-22)
Anthropic's Consumer Terms section 3 bars relying on the service to buy or sell securities, or to give or receive advice about
securities, commodities, derivatives or other financial products, because Anthropic is not a broker-dealer or registered
investment adviser. Placing orders was already refused in code (Q-018, desk-trade.py). From today the Claude writer also leaves
domains 09 and 10 empty and never writes a lean, slug, ticker or money tag aimed at a tradable contract; it says so under
Silences. This is a structural line, not a judgement per item, and it is only about the Claude seat. Codex, Grok, DeepSeek and
the organizer are governed by their own providers' terms and are unchanged. Jaron has the open question of how far the
"receive advice" half reaches; this is the conservative version while it is open.

GPT-6 SOL AND LUNA (2026-09-22, ~2:17 PM ET)
OpenAI announced GPT-6 Sol and GPT-6 Luna, described as bringing GPT-6 Astra's strengths into faster and cheaper models.
Tested the same hour from the MSI: `codex exec -m gpt-6-luna` and `-m gpt-6-sol` both return
"The 'gpt-6-<name>' model is not supported when using Codex with a ChatGPT account."
That is a plan refusal, not an unknown-model error, so the ids are real and the ChatGPT-account path does not carry them yet
(Astra rolled out to API/enterprise first too). RESOLVED the same afternoon. The refusal was a stale CLI, not a plan limit: Jaron saw 6 Luna and 6 Sol in the Codex app's
model picker, the CLI was on 0.153.4 while 0.155.1 was out, and after `scoop update codex` the same call returned normally.
Prices from OpenAI's own card: Astra $10/$50, Sol $2/$10, Luna $0.10/$0.50 per million - GPT-6 Luna is HALF the price of
GPT-5.6 Luna ($0.20/$1.20) and built on Astra. OpenAI says the 50% cut is permanent and makes subscription usage go further
too. The 07:30 watch writer is pinned to gpt-6-luna as of 2026-09-22 (collectors/run_codex.ps1). Lesson worth keeping: when a
model is refused by name, check the client version before believing the refusal.

EFFORT DOES NOT FOLLOW THE MODEL FLAG (2026-09-23)
Measured, not guessed. `~/.codex/config.toml` sets `model_reasoning_effort = "max"`, but passing `-m gpt-6-luna` on the
command line does not carry it: the 2026-09-23 07:32 run reported "reasoning effort: high" in its own header. Result, same
task and same 24 headings: 09-22 on 5.6 Luna at max produced 49 observed items and 59 source URLs in 19,554 bytes; 09-23 on
6 Luna at high produced 17 observed items and 23 sources in 9,399 bytes. Less than half.
GPT-6 Luna does accept max when it is passed explicitly (`-c model_reasoning_effort=max`), so this was a harness mistake by
Claude Code on 09-22, not a weaker model. The runner now passes both flags together. The 5.6-vs-6 comparison is INCONCLUSIVE
until a max-effort 6 Luna run exists; 09-24 is the first clean one.
Rule: when you pin a model on the command line, pin the effort with it, and read the run header to confirm what actually ran.

