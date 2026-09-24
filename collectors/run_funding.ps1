# Funding lane (the rebuilt Revenue Desk). Runs offers\agent-funding\TASK.txt on Codex (GPT-6 Luna, max effort, live web search,
# ChatGPT subscription - not API credits) and pushes whatever it found, drafted, or submitted.
# Registered 2026-09-24 by Claude Code as the Windows task "Watch Funding Lane", daily 2:00 PM (outside the 6:30-9:10 AM block).
$ErrorActionPreference = "Continue"
Set-Location "C:\Users\lilli\Projects\watch"
git pull --rebase 2>&1 | Out-Null
$day = (Get-Date).ToString("yyyy-MM-dd")
$prompt = (Get-Content offers\agent-funding\TASK.txt -Raw) + "`n`nRun note from the MSI: you are running as codex exec on the machine. Work inside offers/agent-funding/. Today is $day. The caller commits and pushes when you finish."
$tmp = Join-Path $env:TEMP "watch-funding-prompt.txt"
Set-Content -Path $tmp -Value $prompt -Encoding UTF8
$log = Join-Path $env:TEMP "watch-funding-run.log"
Get-Content $tmp | & codex --search exec -m gpt-6-luna -c model_reasoning_effort=max -s workspace-write --skip-git-repo-check -C "C:\Users\lilli\Projects\watch" - > $log 2>&1
$changed = (git status --porcelain offers/agent-funding | Measure-Object).Count
Add-Content -Path "collectors\funding_runs.log" -Value ("{0} | files changed: {1} | last line: {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $changed, ((Get-Content $log -Tail 1) -join " "))
git add -A
git commit -m "funding: $day" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" 2>&1 | Out-Null
git push 2>&1 | Out-Null
