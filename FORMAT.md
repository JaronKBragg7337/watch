# Capture format — every writer, every day

File: `<writer>/YYYY-MM-DD.md` (local date, America/Indiana/Indianapolis). Hourly writers use `YYYY-MM-DD-HH.md`.

```
# <writer> capture — YYYY-MM-DD
Writer: <grok|claude|codex|perplexity|deepseek|qwen|kimi> | Model: <name/version if known> | Time: <local time>
Window: last 24h (or the hours covered) | Sources: <web | X | video | official accounts | other captures (reader)>
Status: substantive | thin | unavailable

## 01 crypto / on-chain / stablecoins
## 02 stocks / macro / rates / labor
## 03 AI / models / infra / pricing of intelligence
## 04 energy / grid / compute power / materials
## 05 geopolitics / conflict / borders / law
## 06 companies / hiring / M&A / who is shipping
## 07 demographics / migration / prices on the ground / culture
## 08 supply chain / freight / food / housing inputs
## 09 prediction-market resolution events   (anything that changes how a market resolves: an official sentence, a date, a rule)
## 10 crypto / stock catalysts              (earnings, listings, hacks, ETF flows, halvings, regulation)
## 11 Indiana / Midwest ground truth        (cost of living, weather, local employers, roofing season, state agencies)

Each item, one line:
- [HH:MM local] [observed|claim|theory] [official|press|solo|social|model-only] what happened — source URL — money: <polymarket slug | ticker | asset | none>
  observed = a primary source said/did it; claim = someone asserts it, not confirmed; theory = a pattern or scenario, unconfirmed.
  source class (Jaron, 2026-09-18): official = a government/company/venue speaking for itself; press = an outlet; solo = an independent
  journalist or researcher; social = X/forums; model-only = the writer's own knowledge with no source. A class is a label, not a rank —
  solo and social have carried things official channels had not said yet.

## Persistence
Items that appeared in earlier captures and are back (say which date). Not confirmation.

## Silences
What usually shows up and did not.

## Could not see
Sources down, refused, paywalled, outside the writer's reach. Say it.
```

Readers (deepseek, qwen) use the same headings but `Sources: other captures (reader)`, and add:
`## Convergence` (what two or more collectors agree on), `## Divergence` (where they disagree, kept), and
`## From the other hemisphere` (what a non-US reader would weigh differently).
