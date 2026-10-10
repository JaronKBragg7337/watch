# First Light (Kimi, Eastern Hemisphere desk) - runs kimi/TASK.txt headless with the Kimi Code CLI on Jaron's Allegretto plan
# (logged in 2026-10-09; RECONNECT.md section 8). Live web search is built in. Registered as "Watch Kimi First Light", daily 06:30.
$ErrorActionPreference = "Continue"
Set-Location "C:\Users\lilli\Projects\watch"
git pull --rebase 2>&1 | Out-Null
$day = (Get-Date).ToString("yyyy-MM-dd")
# Short one-line prompt: Windows PowerShell 5 mangles long multi-line args with quotes to native exes (10/10 run failed: "unknown command Eastern").
$prompt = "Read the file kimi/TASK.txt in this folder and do exactly what it says. Today is $day. Write the file kimi/$day.md and stop; the caller commits and pushes."
$log = Join-Path $env:TEMP "watch-kimi-run.log"
& "$env:USERPROFILE\.kimi-code\bin\kimi.exe" -p $prompt > $log 2>&1
$ok = Test-Path "kimi\$day.md"
$tail = if ($ok) { "wrote kimi/$day.md ($((Get-Item "kimi\$day.md").Length) bytes)" } else { "NO FILE; last log line: " + ((Get-Content $log -Tail 1) -join " ") }
Add-Content -Path "collectors\kimi_runs.log" -Value ("{0} | {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $tail)
if ($ok) { python collectors\first_light_adds.py $day 2>&1 | Out-Null }
git add -A
git commit -m "watch: kimi (First Light) $day" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" 2>&1 | Out-Null
git push 2>&1 | Out-Null
