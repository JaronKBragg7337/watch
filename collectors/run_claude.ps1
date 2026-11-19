# Claude desk capture for the daily watch, as a Windows task ("Watch Claude Desk", daily 03:00 local).
# 11/5/2026: the desktop-app scheduled task "watch-collect" silently stopped after 10/31, so claude/ had no capture since 10/28.
# This runs the same instructions (C:\Users\lilli\.claude\scheduled-tasks\watch-collect\SKILL.md) headless with the saved 1-year token,
# like projects/news-show/run_news.ps1 does. Network only, no GPU.
$ErrorActionPreference = "Continue"
$watch = "C:\Users\lilli\Projects\watch"
$log   = "C:\Users\lilli\AI-Shared\projects\news-show\runs.log"
$day   = (Get-Date).ToString("yyyy-MM-dd")
Set-Location $watch
# Skip only a GOOD file (same rule as collectors/source_gate.py). A short, stub or "Status: unavailable" file stays in place
# (it is tracked; deleting it would block the agent's git pull) and the agent is told to replace it. (11/19)
$redo = ""
if (Test-Path "claude\$day.md") {
  $size = (Get-Item "claude\$day.md").Length
  $text = Get-Content "claude\$day.md" -Raw
  $head = (Get-Content "claude\$day.md" -TotalCount 12) -join "`n"
  $stub = ($size -lt 5000) -and ($text -match "(?i)no run took place|did not run|nothing to report today")
  $unavail = $head -match "(?i)\bStatus:\s*unavailable"
  if ($size -ge 3000 -and -not $stub -and -not $unavail) { exit 0 }
  $redo = " NOTE: claude/$day.md already exists but is only $size bytes, a stub, or marked unavailable. Replace it with a full capture: overwrite it, then commit and push."
}
$tokLine = Get-Content "$HOME\.secrets\keys.env" | Where-Object { $_ -match "^CLAUDE_CODE_OAUTH_TOKEN=" } | Select-Object -First 1
if ($tokLine) { $env:CLAUDE_CODE_OAUTH_TOKEN = ($tokLine -split "=",2)[1].Trim().Trim([char]34) }
$prompt = "Read C:\Users\lilli\.claude\scheduled-tasks\watch-collect\SKILL.md and do exactly what it says for today ($day). Stop when claude/$day.md is pushed.$redo"
$out = Join-Path $env:TEMP "watch-claude-desk.log"
& claude -p $prompt --model claude-sonnet-5-5 --permission-mode acceptEdits --add-dir "C:\Users\lilli\AI-Shared" --allowedTools "Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Bash(git:*),Bash(date:*)" > $out 2>&1
$ok = (Test-Path "claude\$day.md") -and ((Get-Item "claude\$day.md").Length -ge 3000)
Add-Content -Path $log -Value ("{0} | claude desk capture {1}: {2}" -f (Get-Date -Format "yyyy-MM-dd HH:mm"), $day, $(if ($ok) { "written" } else { "NO FILE: " + ((Get-Content $out -Tail 1) -join " ") }))
