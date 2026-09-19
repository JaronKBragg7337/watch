# Runs the DeepSeek reader over today's captures and pushes. A plain Windows scheduled task, no AI subscription usage.
# Registered 2026-09-19 as "Watch DeepSeek Reader", daily 09:00 local (after Codex's and Grok's morning captures).
$ErrorActionPreference = "Continue"
Set-Location "C:\Users\lilli\Projects\watch"
git pull --rebase 2>&1 | Out-Null
$env:PYTHONIOENCODING = "utf-8"
$out = & "C:\Users\lilli\scoop\apps\python312\current\python.exe" collectors\deepseek_read.py 2>&1
$day = (Get-Date).ToString("yyyy-MM-dd")
Add-Content -Path "collectors\deepseek_runs.log" -Value ("{0} | {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), ($out -join " ").Substring(0, [Math]::Min(300, ($out -join " ").Length)))
git add -A
git commit -m "watch: deepseek reader $day" -m "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>" 2>&1 | Out-Null
git push 2>&1 | Out-Null
