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

# Search the same 21 domains as the watch capture format. One HTML search per
# domain makes the MSI a second discovery path when feeds do not cover a story.
$searches = @(
    [pscustomobject]@{ Domain = "01 crypto / on-chain / stablecoins"; Query = "cryptocurrency bitcoin ethereum stablecoin news today" },
    [pscustomobject]@{ Domain = "02 stocks / macro / rates / labor"; Query = "markets stocks economy Federal Reserve jobs inflation news today" },
    [pscustomobject]@{ Domain = "03 AI / models / infra / pricing of intelligence"; Query = "AI models OpenAI Anthropic technology news today" },
    [pscustomobject]@{ Domain = "04 energy / grid / compute power / materials"; Query = "energy electricity grid oil gas battery materials news today" },
    [pscustomobject]@{ Domain = "05 geopolitics / conflict / borders / law"; Query = "world geopolitics conflict Iran Ukraine Venezuela Greenland news today" },
    [pscustomobject]@{ Domain = "06 companies / hiring / M&A / who is shipping"; Query = "companies business hiring merger acquisition product launch news today" },
    [pscustomobject]@{ Domain = "07 demographics / migration / prices on the ground / culture"; Query = "demographics migration cost of living culture news today" },
    [pscustomobject]@{ Domain = "08 supply chain / freight / food / housing inputs"; Query = "supply chain shipping freight food housing materials news today" },
    [pscustomobject]@{ Domain = "09 prediction-market resolution events"; Query = "official announcement dates deadline election resolution event news today" },
    [pscustomobject]@{ Domain = "10 crypto / stock catalysts"; Query = "stock earnings crypto ETF hack catalyst listing news today" },
    [pscustomobject]@{ Domain = "11 major US cities and regions"; Query = "major US cities regions Chicago Texas Florida California news today" },
    [pscustomobject]@{ Domain = "12 sports"; Query = "sports injuries lineups schedules NFL NBA MLB news today" },
    [pscustomobject]@{ Domain = "13 U.S. politics and elections"; Query = "US politics elections polls Congress court ruling news today" },
    [pscustomobject]@{ Domain = "14 weather, climate and disasters"; Query = "weather climate storm flood wildfire disaster news today" },
    [pscustomobject]@{ Domain = "15 health"; Query = "health outbreak FDA drug approval public health news today" },
    [pscustomobject]@{ Domain = "16 law, courts and regulation"; Query = "court ruling law regulation SEC FCC legislation news today" },
    [pscustomobject]@{ Domain = "17 outages and cyber"; Query = "cyberattack data breach cloud outage telecom infrastructure news today" },
    [pscustomobject]@{ Domain = "18 disclosure and anomalies"; Query = "UAP UFO declassification government disclosure news today" },
    [pscustomobject]@{ Domain = "19 science and space"; Query = "science space NASA rocket launch discovery news today" },
    [pscustomobject]@{ Domain = "20 entertainment and culture markets"; Query = "entertainment box office awards streaming music news today" },
    [pscustomobject]@{ Domain = "21 uncategorised"; Query = "major world news today latest headlines" }
)
$searchUa = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
$searchFailureCount = 0
foreach ($search in $searches) {
    try {
        $searchUrl = "https://html.duckduckgo.com/html/?q=" + [uri]::EscapeDataString($search.Query)
        $html = (Invoke-WebRequest -Uri $searchUrl -TimeoutSec 20 -MaximumRedirection 5 -UserAgent $searchUa `
            -Headers @{ "Accept" = "text/html,application/xhtml+xml" }).Content
        $resultMatches = [regex]::Matches($html, '(?is)<a\b(?=[^>]*\bclass=["''][^"'']*\bresult__a\b[^"'']*["''])(?=[^>]*\bhref=["'']([^"'']+)["''])[^>]*>(.*?)</a>')
        $added = 0
        foreach ($match in $resultMatches) {
            $link = [System.Net.WebUtility]::HtmlDecode($match.Groups[1].Value)
            $title = [System.Net.WebUtility]::HtmlDecode(($match.Groups[2].Value -replace '(?is)<[^>]+>', '' -replace '\s+', ' ')).Trim()
            $redirect = [regex]::Match($link, '[?&]uddg=([^&]+)')
            if ($redirect.Success) { $link = [uri]::UnescapeDataString($redirect.Groups[1].Value) }
            if ($link.StartsWith('//')) { $link = "https:$link" }
            if ([string]::IsNullOrWhiteSpace($title) -or $link -notmatch '^https?://') { continue }
            $key = ($link.TrimEnd('/') + '|' + $title).ToLowerInvariant()
            if (-not $seen.Add($key)) { continue }
            $host = ([uri]$link).Host -replace '^www\.', ''
            $source = $host
            $official = $host -match '\.(gov|mil)$' -or $host -match '(^|\.)openai\.com$|(^|\.)anthropic\.com$|(^|\.)spacex\.com$'
            $label = if ($official) { "observed" } else { "claim" }
            $items.Add([pscustomobject]@{ Title = $title; Source = $source; Url = $link; Class = $(if ($official) { "official" } else { "press" }); Label = $label; Time = $now.ToString('HH:mm'); Domain = $search.Domain })
            $added++
            if ($added -ge 2) { break }
        }
        if ($added -eq 0) {
            $searchFailureCount++
            $unavailable.Add("DuckDuckGo search for $($search.Domain): no usable results ($searchUrl)")
            $items.Add([pscustomobject]@{ Title = "MSI search attempted; DuckDuckGo returned no usable headlines for this domain."; Source = "MSI search attempt"; Url = $searchUrl; Class = "model-only"; Label = "observed"; Time = $now.ToString('HH:mm'); Domain = $search.Domain })
        }
    } catch {
        $searchFailureCount++
        $unavailable.Add("DuckDuckGo search for $($search.Domain): unavailable ($searchUrl)")
        $items.Add([pscustomobject]@{ Title = "MSI search attempted; DuckDuckGo was unavailable for this domain."; Source = "MSI search attempt"; Url = $searchUrl; Class = "model-only"; Label = "observed"; Time = $now.ToString('HH:mm'); Domain = $search.Domain })
    }
    Start-Sleep -Milliseconds 2200
}

function Get-Domain([object]$item) {
    if ($item.Domain) { return $item.Domain }
    $title = $item.Title
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
    $domain = Get-Domain $item
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
$headlineCount = @($items | Where-Object { $_.Source -ne "MSI search attempt" }).Count
$status = if ($headlineCount -ge 12) { "substantive" } elseif ($headlineCount -gt 0) { "thin" } else { "unavailable" }
$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("# msi capture — $day")
$lines.Add("Writer: msi | Model: RSS/Atom + DuckDuckGo HTML collector | Time: $($now.ToString('HH:mm')) | Window: last 36h of feed entries and today's domain searches | Sources: official RSS/Atom feeds and DuckDuckGo HTML on the MSI")
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
$lines.Add("The capture does not assess stories absent from its readable feeds or searches.")
$lines.Add($(if ($searchFailureCount -gt 0) { "DuckDuckGo returned no usable headlines for $searchFailureCount of 21 domain searches; each attempt is listed in its domain and under Could not see." } else { "All 21 DuckDuckGo domain searches returned usable headlines." }))
$lines.Add("")
$lines.Add("## Could not see")
if ($unavailable.Count) { foreach ($entry in $unavailable) { $lines.Add("- $entry") } } else { $lines.Add("- No configured feed failed.") }

$outDir = Join-Path $watch "msi"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$outPath = Join-Path $outDir "$day.md"
Set-Content -Path $outPath -Value $lines -Encoding UTF8
Write-Output "wrote msi/$day.md: $($items.Count) headlines/search records; $($feeds.Count) configured feeds"

git add -- "msi/$day.md"
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -m "watch: msi $day" -m "Co-Authored-By: Codex <noreply@openai.com>" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Could not commit msi/$day.md" }
    git push | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Could not push msi/$day.md" }
}
