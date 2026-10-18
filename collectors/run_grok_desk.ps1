# Grok Build (desk) - Meridian desk / blind-spot check (Claude Code 2026-10-18). SuperGrok meter, not Claude's.
$ErrorActionPreference = "Continue"
Set-Location "C:\Users\lilli\Projects\watch"
git pull --rebase 2>&1 | Out-Null
$day = (Get-Date).ToString("yyyy-MM-dd")
$prompt = "Read the file grok/TASK.txt in this folder and do exactly what it says. Today is $day. Write the file and stop; the caller commits and pushes."
$log = Join-Path $env:TEMP "watch-grok-desk-run.log"
& "$env:USERPROFILE\.grok\bin\grok.exe" -p $prompt --always-approve --max-turns 60 --no-memory > $log 2>&1
$ok = Test-Path "grok\$day.md"
$tail = if ($ok) { "wrote grok\$day.md" } else { "NO FILE; last log line: " + ((Get-Content $log -Tail 1) -join " ") }
Add-Content -Path "collectors\grok_runs.log" -Value ("{0} | desk | {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $tail)
git add -A
git commit -m "watch: grok (desk) $day" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" 2>&1 | Out-Null
git push 2>&1 | Out-Null
