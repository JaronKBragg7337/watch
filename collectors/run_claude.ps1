# Claude desk capture for the daily watch, as a Windows task ("Watch Claude Desk", daily 03:00 local).
# 11/5/2026: the desktop-app scheduled task "watch-collect" silently stopped after 10/31, so claude/ had no capture since 10/28.
# This runs the same instructions (C:\Users\lilli\.claude\scheduled-tasks\watch-collect\SKILL.md) headless with the saved 1-year token,
# like projects/news-show/run_news.ps1 does. Network only, no GPU.
$ErrorActionPreference = "Continue"
$watch = "C:\Users\lilli\Projects\watch"
$log   = "C:\Users\lilli\AI-Shared\projects\news-show\runs.log"
$day   = (Get-Date).ToString("yyyy-MM-dd")
Set-Location $watch
if (Test-Path "claude\$day.md") { exit 0 }
$tokLine = Get-Content "$HOME\.secrets\keys.env" | Where-Object { $_ -match "^CLAUDE_CODE_OAUTH_TOKEN=" } | Select-Object -First 1
if ($tokLine) { $env:CLAUDE_CODE_OAUTH_TOKEN = ($tokLine -split "=",2)[1].Trim().Trim([char]34) }
$prompt = "Read C:\Users\lilli\.claude\scheduled-tasks\watch-collect\SKILL.md and do exactly what it says for today ($day). Stop when claude/$day.md is pushed."
$out = Join-Path $env:TEMP "watch-claude-desk.log"
& claude -p $prompt --permission-mode acceptEdits --add-dir "C:\Users\lilli\AI-Shared" --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Bash(git:*),Bash(date:*)" > $out 2>&1
$ok = Test-Path "claude\$day.md"
Add-Content -Path $log -Value ("{0} | claude desk capture {1}: {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $day, $(if ($ok) { "written" } else { "NO FILE: " + ((Get-Content $out -Tail 1) -join " ") }))
