# Rift Clash — itch.io listing draft

**Status:** draft only · bots/solo as-is · no repo/deploy edits  
**Play now:** https://rift-clash.vercel.app  
**Repo:** https://github.com/JaronKBragg7337/rift-clash  
**Suggested price:** Free (or PWYW $0+) for bots/solo launch; optional tip jar. Human MP is *not* in this SKU until a hosted server exists.

---

## Title
**Rift Clash**

## Short description (itch blurb ≤140 chars)
Browser League-style 5v5 MOBA. 16 champs, full items/jungle/vision, and bots so you can play a complete match solo — no install.

## Genre tags
`moba` · `multiplayer` · `browser` · `strategy` · `action` · `3d` · `procedural` · `webgl`

## Kind of project
Game · Browser / HTML5 · Windows / Mac / Linux (any modern browser)

## Long description

### What it is
**Rift Clash** is a browser-based, League of Legends–inspired MOBA. You get a Summoner's Rift–style three-lane map, server-authoritative combat, and a full bot roster so a complete 5v5 match works **solo with no backend**.

The live Vercel build needs **no server** for Play vs Bots — the same authoritative simulation that runs on Node also runs inside your tab.

### What's in this build
- **16 champions** with unique passives and QWER kits (not reskins)
- **60+ items** with build paths, mythics, actives, and a full shop
- **Jungle + objectives** — camps, scuttle, Herald, Baron, elemental drakes + Soul
- **Vision** — fog, brush, wards, stealth / true sight
- **Bots** — three difficulty tiers; lane, farm, jungle, gank, buy, level, kite, retreat
- **Match flow** — champ select → load → match → post-game scoreboard / MVP
- **Procedural everything** — models, VFX, audio synthesized at runtime (no binary art pack)

### Controls (summary)
Right-click move/attack · A-click attack-move · QWER abilities · D/F summoners · 1–6 items · B recall · P shop · Tab scoreboard · G ping wheel · Y camera lock · Space center · Shift+S surrender. All rebindable in Settings.

### How to play
1. Open https://rift-clash.vercel.app  
2. Choose **Play vs Bots**  
3. Pick a champion and role — remaining slots fill with bots  

*(Human multiplayer is supported by the codebase but needs a running game server. This itch page ships the **bots/solo static experience** only.)*

### Known limits (honest)
- Procedural low-poly models and synthesized “voice” barks — not authored VO/art
- Bots are competent, not expert coordinated five-mans
- No accounts, ranked matchmaking, or reconnect-to-match in this SKU

### Tech note for curious players
Node + Socket.IO authoritative sim · Three.js client · 30 Hz sim / 20 Hz snapshots · shared map def so server and client never disagree on geometry.

### Credits / license
Made by Jaron K. Bragg / Heartbeat Observatory. Listing text is a draft for empire launch order item (3). Confirm license/pricing with Jaron before publish. Q-006 payment rail still owner-auth if you want paid tips or a future MP tier.

---

## Suggested itch metadata
| Field | Value |
| --- | --- |
| Classification | Games |
| Release status | Prototype / In development (playable) |
| Pricing | Free · optional donations |
| Platforms | HTML5 |
| Accessibility | Keyboard remappable; mouse required |

## Screenshots / trailer TODO (not in this draft)
Capture: champ select, mid-lane fight, dragon pit, shop UI, post-game board. Optional 30s silent GIF of a bot match.
