# Runs the Codex writer (codex/TASK.txt) from the MSI and pushes the capture. Codex CLI is signed in as auth_mode=chatgpt, so this
# runs on Jaron's ChatGPT subscription (Luna model per ~/.codex/config.toml), not API credits. Live web search on.
# Registered 2026-09-21 as "Watch Codex Writer", daily 07:30 local. Replaces the "paste TASK.txt into ChatGPT" step.
$ErrorActionPreference = "Continue"
Set-Location "C:\Users\lilli\Projects\watch"
git pull --rebase 2>&1 | Out-Null
$day = (Get-Date).ToString("yyyy-MM-dd")
$prompt = (Get-Content codex\TASK.txt -Raw) + "`n`nRun note from the MSI: you are running as codex exec on the machine, not as a ChatGPT scheduled task. Write the file codex/$day.md and stop; the caller commits and pushes. Today is $day."
$tmp = Join-Path $env:TEMP "watch-codex-prompt.txt"
Set-Content -Path $tmp -Value $prompt -Encoding UTF8
$log = Join-Path $env:TEMP "watch-codex-run.log"
Get-Content $tmp | & codex --search exec -s workspace-write --skip-git-repo-check -C "C:\Users\lilli\Projects\watch" - > $log 2>&1
$ok = Test-Path "codex\$day.md"
$tail = if ($ok) { "wrote codex/$day.md ($((Get-Item "codex\$day.md").Length) bytes)" } else { "NO FILE; last log line: " + ((Get-Content $log -Tail 1) -join " ") }
Add-Content -Path "collectors\codex_runs.log" -Value ("{0} | {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $tail)
git add -A
git commit -m "watch: codex $day" -m "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" 2>&1 | Out-Null
git push 2>&1 | Out-Null
