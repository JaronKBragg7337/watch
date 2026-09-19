# Rift Clash — always-on MP server cost estimate (one page)

**Status:** estimate only · **do not provision** · CPU/RAM/mo tiers  
**Scope:** optional human-vs-human lobby for the existing Node game server (`npm start` / port 3001). Static bots/solo stays on Vercel free of this bill.  
**Assumptions from README:** authoritative Node sim, Socket.IO, shared lobby (no full matchmaking service), remaining slots fill with bots; headless 10-bot match ~20× realtime on a modern desktop at 30 tick/s.

---

## What you are buying
One always-on Linux box (or equivalent) that runs the Rift Clash **game server** 24/7 so remote players can open:

`https://rift-clash.vercel.app/?server=wss://<your-host>`

Not included in this page: accounts, ranked MM, multi-region, Redis, managed DB, CDN for the client (client stays on Vercel).

---

## Sizing heuristics
| Concurrent matches (rough) | CCU ballpark | Suggested floor |
| --- | --- | --- |
| 1 lobby / 1 match | ~10 | 1 vCPU · 1–2 GB RAM |
| 2–3 matches | ~20–30 | 2 vCPU · 2–4 GB RAM |
| Busy evening hobby crowd | ~50–100 | 2–4 vCPU · 4–8 GB RAM + watch egress |

Bandwidth is the usual surprise: tick-rate snapshots × players × hours. Budget VPS with fat included transfer usually beats big-cloud egress for this shape of game.

---

## Monthly tiers (USD, public list prices ≈ mid-2026 indie VPS — verify before buy)

| Tier | Spec (CPU / RAM) | Role | Indicative $/mo | Notes |
| --- | --- | --- | --- | --- |
| **T0 Dev** | 1 vCPU / 1 GB | LAN + friends smoke test | **$4–6** | Fine for “is MP still green”; not a launch SLA |
| **T1 Soft launch** | 1 vCPU / 2 GB | 1–2 concurrent matches | **$6–12** | Sweet spot for itch “optional MP” footnote |
| **T2 Small community** | 2 vCPU / 4 GB | Several matches / ~30–50 CCU | **$12–24** | Headroom for bots + a few human lobbies |
| **T3 Busy evenings** | 4 vCPU / 8 GB | ~50–100 CCU hobby peaks | **$24–48** | Still one box; no multi-region |
| **Cloud “escape hatch”** | 2–4 vCPU / 4–8 GB | Same as T2–T3 on AWS/GCP/Azure | **~$30–120+** | Easier scale-out later; egress often dominates |

Figures are **compute only** (CPU/RAM/mo). Add separately if you insist: domain/TLS (~$0–15/yr), observability (~$0–10), backups (~$1–5). Do **not** provision any of this until Jaron okays spend (Q-006 still owner auth for money rails; this is ops cost, not Stripe).

---

## Recommendation for launch order item (3)
Ship itch as **bots/solo** with zero always-on cost. If someone asks for human MP, stand up **T1** first (~$6–12/mo), point Vercel client with `?server=`, and measure real CCU for a week before jumping tiers.

**Non-goals until measured:** Agones/K8s, multi-region, dedicated matchmaking service, Redis cluster — those belong after T2 is actually full.

---

## Open decisions (owner)
1. Approve any paid always-on box at all?  
2. If yes: T1 vs T2 for first month?  
3. Operator: Jaron / Claude Code / Bridge observe-only — who gets SSH and restart duty?
