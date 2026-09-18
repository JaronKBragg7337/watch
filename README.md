# watch — one place every AI's daily watch lands

Jaron's rule (2026-09-18): every AI that can run a schedule writes a daily capture HERE, in one format. One Grok organizes them
into a daily brief and a short market feed. The trading bot reads that when it decides. Orchestra's scope, official-watch-briefs'
plumbing, no new rules.

## Who writes what
| folder | writer | how it gets here | sees the web? | role |
|---|---|---|---|---|
| `grok/` | Grok scheduled task | pushes directly (as official-watch-briefs does) | yes, plus X and video | collector |
| `claude/` | Claude Code scheduled task on the MSI (`watch-collect`, daily) | commits + pushes | yes (web search) | collector |
| `codex/` | Codex cloud scheduled task | commits to this repo | yes | collector |
| `perplexity/` | Perplexity Tasks | email → MSI relay commits (or the API once a key exists) | yes | collector |
| `deepseek/` | `collectors/deepseek_read.py` on the MSI (API credits) | commits | **no** — reads the day's captures | Eastern reader |
| `qwen/` | local Ollama on the MSI | commits | no | reader / summariser |
| `kimi/` | Kimi scheduled task (later, needs subscription) | tbd | yes | Eastern collector |
| `brief/` | the organizer Grok bot | reads every folder for the day, writes one brief | — | organizer |
| `market-feed/` | the organizer | short packets for the trading bots (`YYYY-MM-DD.jsonl`) | — | organizer |

`official-watch-briefs` stays exactly as it is — the clean official-sources-only instrument. Nothing here replaces it.

## The format
`FORMAT.md`. Same headings for every writer so the organizer does not care who wrote it. Every item is labelled
observed / claim / theory, with a time and a link, and a `money:` tag when it touches a market, an asset, or a resolution rule.

## The rules — Jaron's, not a lab's
1. No topic bans. Unofficial, theory, rumour, markets, disclosure, collapse — all allowed, all labelled.
2. Nothing is deleted for being unofficial. A reader may filter for a consumer; the capture stays.
3. "I could not see this" is an entry, not silence.
4. Collectors never see positions or P&L. Positions may tell the organizer WHICH markets to include, never what to conclude
   (ESTIMATION-ISOLATION.md in AI-Shared — the March Orchestra lesson).
5. Persistence is logged. Confirmation is a separate field. A thing that keeps coming back is not thereby true.
6. Only the trading Grok touches money. Collectors write files.

## Consumers
- Live Wire (Polymarket US, fast lane) reads `market-feed/` + `brief/` as reference.
- A Kraken lane (stocks / crypto, slow, only with a news source attached) reads the same — after this works.
