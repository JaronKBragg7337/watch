# Runs the Codex writer (codex/TASK.txt) from the MSI and pushes the capture. Codex CLI is signed in as auth_mode=chatgpt, so this
# runs on Jaron's ChatGPT subscription, not API credits. Live web search on.
# 2026-09-22: pinned to gpt-6-luna. Half the price of 5.6 Luna ($0.10/$0.50 per million vs $0.20/$1.20) and built on GPT-6
# Astra. The CLI needed 0.155.1 to reach it; 0.153.4 refused with 'not supported when using Codex with a ChatGPT account'.
# Jaron's own config.toml still says gpt-5.6-luna for his interactive runs - left alone on purpose, that is his to change.
# 2026-09-23: effort is now passed EXPLICITLY. Passing -m on the command line does NOT inherit model_reasoning_effort from
# config.toml - the 09-23 run silently dropped from max to high and the capture came out less than half the size of 09-22
# (17 observed items vs 49, 23 sources vs 59, same 24 headings). Always pass both -m and -c together.
# Registered 2026-09-21 as "Watch Codex Writer", daily 07:30 local. Replaces the "paste TASK.txt into ChatGPT" step.
$ErrorActionPreference = "Continue"
Set-Location "C:\Users\lilli\Projects\watch"
git pull --rebase 2>&1 | Out-Null
$day = (Get-Date).ToString("yyyy-MM-dd")
$prompt = (Get-Content codex\TASK.txt -Raw) + "`n`nRun note from the MSI: you are running as codex exec on the machine, not as a ChatGPT scheduled task. Write the file codex/$day.md and stop; the caller commits and pushes. Today is $day."
$tmp = Join-Path $env:TEMP "watch-codex-prompt.txt"
Set-Content -Path $tmp -Value $prompt -Encoding UTF8
$log = Join-Path $env:TEMP "watch-codex-run.log"
Get-Content $tmp | & codex --search exec -m gpt-6-luna -c model_reasoning_effort=max -s workspace-write --skip-git-repo-check -C "C:\Users\lilli\Projects\watch" - > $log 2>&1
$ok = Test-Path "codex\$day.md"
$tail = if ($ok) { "wrote codex/$day.md ($((Get-Item "codex\$day.md").Length) bytes)" } else { "NO FILE; last log line: " + ((Get-Content $log -Tail 1) -join " ") }
Add-Content -Path "collectors\codex_runs.log" -Value ("{0} | {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $tail)
git add -A
git commit -m "watch: codex $day" -m "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" 2>&1 | Out-Null
git push 2>&1 | Out-Null
