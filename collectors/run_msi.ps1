# Captures public RSS/Atom headlines from the MSI for the daily watch.
# Registered as "Watch MSI Reader", daily 07:00 local.
$ErrorActionPreference = "Stop"
$watch = "C:\Users\lilli\Projects\watch"
Set-Location $watch

$day = (Get-Date).ToString("yyyy-MM-dd")
$now = Get-Date
$feeds = @(
    [pscustomobject]@{ Name = "AP"; Url = "https://apnews.com/apf-topnews?output=1"; Class = "press" },
    [pscustomobject]@{ Name = "Reuters"; Url = "https://feeds.reuters.com/reuters/worldNews"; Class = "press" },
    [pscustomobject]@{ Name = "BBC World"; Url = "https://feeds.bbci.co.uk/news/world/rss.xml"; Class = "press" },
    [pscustomobject]@{ Name = "NPR"; Url = "https://feeds.npr.org/1004/rss.xml"; Class = "press" },
    [pscustomobject]@{ Name = "Al Jazeera"; Url = "https://www.aljazeera.com/xml/rss/all.xml"; Class = "press" },
    [pscustomobject]@{ Name = "ISW / Critical Threats"; Url = "https://www.understandingwar.org/rss.xml"; Class = "press" },
    [pscustomobject]@{ Name = "Ars Technica"; Url = "https://feeds.arstechnica.com/arstechnica/index"; Class = "press" },
    [pscustomobject]@{ Name = "The Verge"; Url = "https://www.theverge.com/rss/index.xml"; Class = "press" },
    [pscustomobject]@{ Name = "OpenAI"; Url = "https://openai.com/news/rss.xml"; Class = "official" }
)

$items = [System.Collections.Generic.List[object]]::new()
$unavailable = [System.Collections.Generic.List[string]]::new()
$seen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
foreach ($feed in $feeds) {
    try {
        $response = Invoke-WebRequest -Uri $feed.Url -TimeoutSec 20 -MaximumRedirection 5 `
            -UserAgent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36" `
            -Headers @{ "Accept" = "application/rss+xml, application/atom+xml, application/xml, text/xml" }
        [xml]$xml = $response.Content
        $nodes = $xml.SelectNodes("//*[local-name()='item' or local-name()='entry']")
        if (-not $nodes -or $nodes.Count -eq 0) { throw "No RSS/Atom entries" }
        foreach ($node in $nodes) {
            $title = [System.Net.WebUtility]::HtmlDecode([string]$node.SelectSingleNode("./*[local-name()='title']")?.InnerText)
            $urlNode = $node.SelectSingleNode("./*[local-name()='link']")
            $link = [string]$urlNode?.InnerText
            if (-not $link -and $urlNode -and $urlNode.Attributes["href"]) { $link = [string]$urlNode.Attributes["href"].Value }
            if ([string]::IsNullOrWhiteSpace($title) -or [string]::IsNullOrWhiteSpace($link)) { continue }
            $dateNode = $node.SelectSingleNode("./*[local-name()='pubDate' or local-name()='published' or local-name()='updated' or local-name()='date']")
            $published = $now
            if ($dateNode) {
                $parsed = [DateTimeOffset]::MinValue
                if ([DateTimeOffset]::TryParse([string]$dateNode.InnerText, [ref]$parsed)) { $published = $parsed.LocalDateTime }
            }
            if ($published -lt $now.AddHours(-36)) { continue }
            $key = ($link.TrimEnd('/') + '|' + ($title -replace '\s+', ' ').Trim()).ToLowerInvariant()
            if (-not $seen.Add($key)) { continue }
            $label = if ($feed.Class -eq "official") { "observed" } else { "claim" }
            $items.Add([pscustomobject]@{ Title = ($title -replace '\s+', ' ').Trim(); Source = $feed.Name; Url = $link; Class = $feed.Class; Label = $label; Time = $published.ToString('HH:mm') })
        }
    } catch {
        $unavailable.Add("$($feed.Name): feed unavailable or unreadable ($($feed.Url))")
    }
}

function Get-Domain([string]$title) {
    if ($title -match '(?i)iran|israel|ukraine|russia|war|missile|gaza|venezuela|greenland|border|ceasefire|nato|military|attack|troops|diplomat') { return "05 geopolitics / conflict / borders / law" }
    if ($title -match '(?i)bitcoin|crypto|ethereum|stablecoin|blockchain|coinbase|token') { return "01 crypto / on-chain / stablecoins" }
    if ($title -match '(?i)stock|market|fed |federal reserve|inflation|jobs report|treasury|rates|economy|payroll') { return "02 stocks / macro / rates / labor" }
    if ($title -match '(?i)openai|anthropic|artificial intelligence|\bAI\b|chatgpt|claude|model|chip|data center|cloud computing') { return "03 AI / models / infra / pricing of intelligence" }
    if ($title -match '(?i)oil|energy|power grid|electricity|solar|nuclear|gas prices|battery|lithium') { return "04 energy / grid / compute power / materials" }
    if ($title -match '(?i)company|business|earnings|merger|layoff|ceo|launches|product|revenue|acquisition') { return "06 companies / hiring / M&A / who is shipping" }
    if ($title -match '(?i)migration|housing|prices|cost of living|population|culture') { return "07 demographics / migration / prices on the ground / culture" }
    if ($title -match '(?i)supply chain|shipping|freight|food|grain|port|factory|housing|china.*(export|trade|tariff)|rare earth') { return "08 supply chain / freight / food / housing inputs" }
    if ($title -match '(?i)polymarket|prediction market|resolution|election date|deadline') { return "09 prediction-market resolution events" }
    if ($title -match '(?i)hack|cyber|outage|breach|ransomware|internet down|cloudflare') { return "17 outages and cyber" }
    if ($title -match '(?i)weather|storm|hurricane|flood|wildfire|earthquake|climate') { return "14 weather, climate and disasters" }
    if ($title -match '(?i)health|virus|outbreak|FDA|vaccine|hospital|drug approval') { return "15 health" }
    if ($title -match '(?i)court|judge|lawsuit|ruling|regulation|SEC|FCC|bill signed') { return "16 law, courts and regulation" }
    if ($title -match '(?i)NASA|space|rocket|satellite|astronomy|planet|launch') { return "19 science and space" }
    if ($title -match '(?i)sport|NFL|NBA|MLB|NHL|soccer|World Cup|Olympic') { return "12 sports" }
    if ($title -match '(?i)film|movie|music|album|box office|streaming|actor|award') { return "20 entertainment and culture markets" }
    return "21 uncategorised"
}

$sections = @{}
foreach ($item in $items) {
    $domain = Get-Domain $item.Title
    if (-not $sections.ContainsKey($domain)) { $sections[$domain] = [System.Collections.Generic.List[string]]::new() }
    $sections[$domain].Add("- [$($item.Time) local] [$($item.Label)] [$($item.Class)] $($item.Title) — $($item.Source) — $($item.Url) — money: none")
}
$headings = @(
    "01 crypto / on-chain / stablecoins", "02 stocks / macro / rates / labor", "03 AI / models / infra / pricing of intelligence",
    "04 energy / grid / compute power / materials", "05 geopolitics / conflict / borders / law", "06 companies / hiring / M&A / who is shipping",
    "07 demographics / migration / prices on the ground / culture", "08 supply chain / freight / food / housing inputs",
    "09 prediction-market resolution events", "10 crypto / stock catalysts", "11 major US cities and regions", "12 sports",
    "13 U.S. politics and elections", "14 weather, climate and disasters", "15 health", "16 law, courts and regulation",
    "17 outages and cyber", "18 disclosure and anomalies", "19 science and space", "20 entertainment and culture markets", "21 uncategorised"
)
$status = if ($items.Count -ge 12) { "substantive" } elseif ($items.Count -gt 0) { "thin" } else { "unavailable" }
$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("# msi capture — $day")
$lines.Add("Writer: msi | Model: RSS/Atom collector | Time: $($now.ToString('HH:mm')) | Window: last 36h of feed entries | Sources: official RSS/Atom feeds on the MSI")
$lines.Add("Status: $status")
$lines.Add("")
foreach ($heading in $headings) {
    $lines.Add("## $heading")
    if ($sections.ContainsKey($heading)) { foreach ($entry in $sections[$heading]) { $lines.Add($entry) } }
    $lines.Add("")
}
$lines.Add("## Persistence")
$lines.Add("No prior MSI capture was compared.")
$lines.Add("")
$lines.Add("## Silences")
$lines.Add("RSS/Atom headlines only; this capture does not assess stories absent from the feeds.")
$lines.Add("")
$lines.Add("## Could not see")
if ($unavailable.Count) { foreach ($entry in $unavailable) { $lines.Add("- $entry") } } else { $lines.Add("- No configured feed failed.") }

$outDir = Join-Path $watch "msi"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$outPath = Join-Path $outDir "$day.md"
Set-Content -Path $outPath -Value $lines -Encoding UTF8
Write-Output "wrote msi/$day.md: $($items.Count) headlines from $($feeds.Count - $unavailable.Count) readable feeds"

git add -- "msi/$day.md"
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "watch: msi $day" -m "Co-Authored-By: Codex <noreply@openai.com>" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Could not commit msi/$day.md" }
    git push | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Could not push msi/$day.md" }
}
