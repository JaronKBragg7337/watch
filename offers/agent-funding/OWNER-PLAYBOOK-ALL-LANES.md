# Owner playbook — do every funding lane (hand to any AI)
Prepared: 2026-09-20 ~20:20 ET by Elons Twin for Jaron
Purpose: You (or another AI walking you) complete the human-only steps. Elons Twin already drafted text; verified receipts = 0 until money hits a designated wallet.

Hard rules (do not let any AI override):
1. Receive-only. Never share seeds/keys. Never pay a fee to "unlock" a grant. Never connect the receive wallet to a strange dapp to get paid.
2. Disclose the AI is fundraising for Jaron K. Bragg / ACS / Heartbeat Observatory.
3. Do not invent live GOAT/0G/Autonomys integrations. Say "planned" if not live.
4. Log each submit under watch/offers/agent-funding/outreach/ with date + portal + confirmation id.
5. Put verified receipts only in receipts/ after on-chain or wallet proof.

Designated receive-only wallets (PUBLIC):
- BTC: bc1qszpdhrmupcw9ncnjfy2v0v3k3t6t63g54yva9h
- TAO: 5Gnbw28omasTbDQ51G6UJ9CUtiWDKENMYFy49MX3czKM8ZfD
- SOL: F1Rc5a2Dhe3VoddJXogmRYGUvax661N2st7PvsdVeb58
- XRP: rU6CSv286Xf2v6yRw854NAVqD8uTPuBSTe  | destination tag 2650773147 REQUIRED
- Base/EVM USDC: NOT SET YET — you must create/add one for tip jar (Lane D)

Files already on MSI:
- Drafts folder: C:\Users\lilli\Projects\watch\offers\agent-funding\
- P01 GOAT draft: outreach\P01-GOAT-application-DRAFT.md
- P03 Autonomys draft: outreach\P03-AUTONOMYS-application-DRAFT.md
- Master pitch: PITCH.md
- Ledger: PROSPECTS.md
- Wallets: WALLETS.json

---

## LANE A — GOAT AI Builder Grants (fastest $2k-shaped ask)
Portal: https://www.goat.network/builder-program
FAQ: https://www.goat.network/faq/builder-program-faq
Ask: Base Grant ~$2,000 (page also mentions Singularity / larger follow-on — do not claim that tier)
Status: DRAFT ready. Needs demo + your submit.

### A1. Make a short honest demo (2–4 min)
Record with Windows Win+G or OBS. Show, in order:
1. heartbeatobservatory.com open in browser
2. github.com/JaronKBragg7337/watch (README or today brief/market-feed)
3. Live Wire / desk: C:\Users\lilli\AI-Shared\state\live-wire.md OR desk-trade running / polymarket.us positions (cash ~$40 is fine — honesty > hype)
4. Say out loud: "AI agent Elons Twin helps operate; I am Jaron, human principal. GOAT x402 / ERC-8004 integration is planned, not live yet."
Upload unlisted to YouTube/Loom OR attach if the form allows. Save the link.
No dedicated Live Wire demo clip found on disk yet (old Screen Recordings from Jun/Aug are unrelated). Make a new one.

### A2. Fill the GOAT form
Paste from P01-GOAT-application-DRAFT.md. Required honesty lines:
- Product live: yes (Heartbeat + watch + Live Wire desk)
- Revenue path: Polymarket US trading P&L + planned paid offers (Studio Patron / MCP pack)
- GOAT stack: planned x402 payments + ERC-8004 identity — NOT claimed live
- Operator disclosure: AI-assisted application; Jaron is applicant

### A3. After submit
Save confirmation screenshot to outreach\P01-GOAT-SUBMITTED-YYYY-MM-DD.md with confirmation id/email. Tell Elons Twin "P01 submitted" so the ledger flips DRAFT → SENT.

---

## LANE B — Autonomys / Subspace Foundation Grants (no prototype required)
Portal: https://subspace.foundation/grants
Process: https://subspace.foundation/grants/application-process
Status: DRAFT ready at P03-AUTONOMYS-application-DRAFT.md

### B1. Open the official application form on that page
Category: AI-powered dApp / on-chain agents

### B2. Paste from the P03 draft
Use the milestone list as-is. Ask modest milestone funding (compute + build time). Prefer official foundation payout; if crypto, SOL or BTC addresses above.

### B3. Expect slow review
Their docs: up to ~8 weeks to first response, then discovery call. After submit, log outreach\P03-AUTONOMYS-SUBMITTED-YYYY-MM-DD.md and tell Elons Twin.

---

## LANE C — 0G Foundation Ecosystem Growth ($88.88M)
Hub: https://0gfoundation.ai/ecosystem
Guild 2.0: CLOSED — skip Guild.
Main ecosystem fund: rolling; grants often $10k–$1M+ milestone; KYC later.

### C1. Find the real Apply form
On the ecosystem page (or 0G Discord #grants), get the official form URL. Do not invent one. If only Discord intake, post a short pitch + links and ask for the form.

### C2. Form answers (use these)
- Project: Heartbeat Observatory + watch + Live Wire autonomous agent stack
- Category: AI agents
- What you need 0G for: verifiable storage / agent logs / DA for watch captures + trade receipts (planned integration)
- Ask: start mid (e.g. $10k–$25k) milestone-based, not $1M fantasy
- Links: heartbeatobservatory.com · github.com/JaronKBragg7337/watch
- Disclosure: AI agent assists; Jaron principal
- KYC: you will complete when they ask (human only)

### C3. Log submit same as A/B

---

## LANE D — Public tip jar (Shieldz / agent tips)
Why blocked: tip rails settle to an EVM address on Base. You only designated BTC/TAO/SOL/XRP.

### D1. Create a receive-only Base address
In Uphold / Coinbase / Rabby / whatever you already use:
1. Add or show a Base network deposit address that can receive USDC
2. Confirm it is receive-capable and you control it
3. Paste the 0x… address into a chat with Elons Twin OR write it into WALLETS.json as "base_usdc"
Never type a seed phrase into any AI chat.

### D2. Stand up the tip jar (you or Elons Twin after D1)
Browser or curl:
  https://shieldz.cash/api/v1/tip-jars?to=0xYOUR_BASE_ADDRESS&title=Heartbeat+Observatory+%2F+ACS&amounts=5,25,100&website=https://www.heartbeatobservatory.com
Save the returned public tip URL. Put it on heartbeatobservatory.com and in PITCH.md.

### D3. Optional: put tip URL in watch README under Funding

---

## LANE E — Still blocked (do later, not tonight)
- AgentFund (Solana): needs wallet signing to launch a campaign — only with you at the keyboard on MSI, one-time auth
- Virtuals Genesis: often needs VIRTUAL spend + wallet ops — skip until grant-style contact found
- Base Builder Grants: scout/retro (1–5 ETH), not a cold form — ship something Base-visible first
- Gitcoin / RetroPGF: wait for an open round + stronger OSS dependency story

---

## LANE F — Supabase money path (related, not a grant)
Q-021: on payday, before savings transfer:
1. Supabase → Billing → Upgrade Pro (~$25/mo), spend cap ON
2. Settings → Database / Disk → resize (e.g. 8 GB) → save
3. Wait Healthy
4. Tell Claude/Elons Twin: TRUNCATE fly_school / fly_live history + qwen event tables; run desk-trail-sync.py; keep Fly School + Qwen Remote Bridge OFF until one-row-per-exam policy
Trading already works offline via desk-trade.py → state/desk-trail-offline.jsonl

---

## Paste this to the other AI (short starter)
"Walk me through completing every lane in C:\\Users\\lilli\\Projects\\watch\\offers\\agent-funding\\OWNER-PLAYBOOK-ALL-LANES.md. Start with Lane A demo recording, then submit GOAT, then Autonomys, then find 0G form, then help me add a Base USDC receive address for Shieldz. Obey the hard rules at the top. Do not invent integrations. Do not ask for seed phrases."

## After you finish any lane
Message Elons Twin one line: which lane, submitted/yes-no, confirmation id or tip URL. Twin updates PROSPECTS.md and stops burning tokens on re-research.
