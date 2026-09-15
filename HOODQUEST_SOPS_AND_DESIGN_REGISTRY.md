# HoodQuest: Standard Operating Procedures (SOP) & Architecture Decision Registry

**Document Version:** 1.0.0  
**Status:** Canonical Reference & Anti-Regression Ledger  
**Target Chains:** Robinhood Testnet (46630) / Robinhood Mainnet (4663)  

---

## 1. Executive Anti-Regression Covenant

This registry records every binding design decision, audited mechanism, edge-case resolution, and standard operating procedure (SOP) for HoodQuest. 

Whenever a rule, timer, or economic constant is introduced or adjusted, this document must be updated with:
1. **The Exact Specification** (Numbers, Timers, Contract Functions).
2. **The Security/Economic Rationale** (Why this exists, what exploit it prevents).
3. **The User & Market Experience** (What the player and marketplace observe).

---

## 2. Audited Companion System (No Stat-Inflation Drift)

### 2.1 The Audited Reality vs. Speculative Inflation
* **Audited Finding:** Earlier casual discussions suggested companion buffs such as "+15% Gold" or "+10% Critical Strike". **These are NOT part of the audited Tier 1 tokenomics.**
* **The Canonical Economic Role of Companions:**
  Companions exist in the audited smart contract (`HoodQuestCompanions.sol`) as:
  1. **Primary Deflationary Gold Sinks:** Adopting a companion permanently burns Royal Gold Sovereigns (`treasuresContract.burnAdoptionGold`):
     - 🐕 **Camp Hound** (IDs 1–3000): Burns **20 Gold**.
     - 🐈 **Shadow Cat** (IDs 7501–10000): Burns **25 Gold**.
     - 🦅 **Highland Falcon** (IDs 3001–5500): Burns **30 Gold**.
     - 🦉 **Barn Owl** (IDs 5501–7500): Burns **40 Gold**.
     - *Net Burn:* 75% is permanently destroyed (deflationary burn), and 25% is credited to the `freeRebateReserve` for community event budgets.
  2. **Proof-of-Play Crafting Supply Chain (`soloForage`):**
     - Active bonded companions can be sent to forage once per UTC day.
     - Awards **+10 XP** toward companion biological bond rank.
     - Has deterministic on-chain drop rates for Soulbound crafting materials:
       - **Sherwood Yew Wood (#16):** 12.0% chance.
       - **Nottingham Iron (#17):** 8.0% chance.
     - These materials cannot be bought or transferred—they can only be foraged or dropped in quests to feed the Blacksmith weapon forge.
  3. **Bond Ranks (Biological Devotion):**
     - Ranks 1 to 5 based strictly on accrued XP (`petXp`):
       - Rank 1: 0–299 XP (Novice)
       - Rank 2: 300–899 XP (Trained)
       - Rank 3: 900–1799 XP (Loyal)
       - Rank 4: 1800–3649 XP (Devoted)
       - Rank 5: 3650+ XP (Eternal Companion — ~1 year of daily forage)
  4. **Strict Boundary:** No un-audited arbitrary combat multipliers may be introduced to permanent Tier 1 tokens. Any future raid perks (e.g. stealth bonus in Vault Heists) must be defined inside replaceable Tier 2 raid modules (`HoodQuestRaids.sol`), keeping Tier 1 permanent contracts boring and immutable.

### 2.2 Companion Care & Slumber (Zero Permadeath)
* **Rule:** Companions **never die, starve, or disappear**.
* **Slumber Sync:** If a host Outlaw enters Slumber (inactivity without food or questing), the companion also sleeps. The biological aging clock pauses safely with **$0 gas required**. When the owner returns, the companion awakens immediately upon the Outlaw's daily care or forage.

---

## 3. Armory Escrow Vault & Equipping Timers

### 3.1 Escrow Architecture (The "Loaded Character" Model)
* **Equipped Items & Bonded Pets Live in `HoodQuest.sol`:**
  - When an Outlaw equips gear (`HoodQuestTreasures.sol` ERC-1155) or bonds a companion (`HoodQuestCompanions.sol` ERC-721), the tokens are transferred into the **`HoodQuest.sol` Armory Vault** via `safeTransferFrom`.
  - They are mapped to the character's `tokenId` (`equippedSlot[hoodId]` and `hoodBoundPet[hoodId]`).
* **Why Escrow Instead of Personal Wallet?**
  1. **Prevents Hot-Swapping:** A player cannot use 1 Golden Arrow across 50 different Outlaws simultaneously.
  2. **Loaded NFT Value:** When an Outlaw is transferred or sold on the Camp Bazaar, its equipped gear and bonded companion **transfer with the character**. The buyer purchases a complete, battle-ready hero.
* **Found Loot (Un-equipped):**
  - Heist drops (Gold, materials, elixirs) are minted directly to the **player's wallet address** (`rewardRecipient`). They only enter escrow if explicitly equipped.

### 3.2 Debonding & Unequipping Timers
To protect the secondary market and combat integrity, the following cooldowns are enforced on-chain:
1. **Equipment Unequip (24-Hour Maturation):**
   - Calling `initiateUnequip(hoodId, slot)` starts a 24-hour maturation timer.
   - The item cannot be withdrawn until `block.timestamp >= maturesAt`.
   - Calling `finalizeUnequip(hoodId, slot)` returns the ERC-1155 token to the owner.
2. **Companion Debonding (12h Lock + 12h Maturation):**
   - A companion must remain bonded for at least **12 hours** before unbonding can even be initiated (`block.timestamp >= petBondedAt[petId] + 12 hours`).
   - Initiating debond (`initiateDebond`) locks the pet in a **12-hour maturation countdown**.
   - After 12 hours, `finalizeDebond` releases the companion back to the owner's personal wallet.
3. **Post-Transfer Marketplace Lock (24 Hours):**
   - After any Outlaw transfer (`_update`), a 24-hour lock is placed on unequipping (`postTransferUnequipLockedUntil[tokenId] = now + 24 hours`).
   - **Rationale:** Prevents predatory "bait-and-switch" attacks where a seller advertises an Outlaw with high-tier gear, executes an unequip transaction in the same block or right before a marketplace sale, and strips the character naked.

---

## 4. Nottingham Castle Vault Raids & Heists

### 4.1 Gas Fees
* **Do players pay gas to join?**
  - **Yes, for the transaction execution.** Every on-chain state change (`requestActionEvent`, `requestHeistBatch`, or `commitSolsticeManeuver`) is an EVM call on **Robinhood Chain (Arbitrum Nitro L2)**.
  - **Estimated Cost:** Less than **$0.001 (sub-penny)** due to L2 gas compression.
* **Two-Step Commit / Permissionless Resolve:**
  - **Step 1 (Player Action):** Consumes daily stamina, snapshots combat attributes, and registers `targetBlock = currentBlock + 2`.
  - **Step 2 (Settlement):** Anyone (the player, the game frontend auto-resolver, or a keeper bot) can call `resolveHeist` or `resolveActionEvent` once the 2-block entropy window passes.

### 4.2 What Happens If an NFT is Transferred / Sold Mid-Raid?
* **Scenario:** An Outlaw is entered into a heist or waiting raid, and the owner transfers or sells the NFT before resolution.
* **Protection 1: Marketplace Listing is Blocked (`canList` Gating):**
  - Entering a raid increments `pendingGameplayCount[hoodId]`.
  - `canList(hoodId)` returns `false` (`reasonFlags |= 1: PENDING_GAMEPLAY_ACTIVE`).
  - The native Camp Bazaar (`HoodQuestBazaar.sol`) will **revert any listing attempt** while an action is unresolved.
* **Protection 2: Direct Transfers Do Not Steal Rewards (Snapshotted Recipient):**
  - If a player initiates a raid and then immediately executes a direct P2P transfer (`transferFrom`) to another wallet before `resolveHeist` is called:
  - In `HoodQuestRaids.sol`, `req.rewardRecipient` is **snapshotted at the moment of request**.
  - When `resolveHeist` is settled, **all Gold and item drops are transferred directly to the original requester's address**, NOT the new owner.
  - The buyer cannot intercept or steal rewards generated by the seller's stamina.
* **Protection 3: Transfer Auto-Cancels Pending Unlocks:**
  - In `HoodQuest._update`, any pending unequip or debond timers are immediately deleted upon transfer.
  - The new owner cannot exploit in-flight unequip requests initiated by a previous holder.
  - `delegateEpoch` increments, immediately revoking any third-party delegates or bot permissions granted by the previous owner.

---

## 6. Consumable Balance & Anti-Inflation Ceilings

### 6.1 The 1-Elixir-Per-Day Rule (Audited Invariant)
* **Rule:** An Outlaw can consume **at most 1 Greenwood Elixir per UTC day** (`lastElixirDay[hoodId] >= today` reverts).
* **Stamina Mechanics:**
  - Base Stamina: 5 heists per day (free, resets 00:00 UTC).
  - Elixir Stamina: Exactly +5 bonus heists per day.
  - Hard Ceiling: Maximum **10 heists per day per Outlaw** under all circumstances.
  - A player cannot "whale farm" by drinking 50 elixirs in one day on one character.

### 6.2 Hard Statutory Stat Ceilings
To guarantee early 2026 Genesis gear is never rendered obsolete by future expansions:
* **Max Attack:** 45 (statutory ceiling in `HoodQuest.sol`).
* **Max Defense:** 30.
* **Max Stealth:** 30.
* **Max Gold Bonus (`goldBonusBps`):** Hard capped at **4000 BPS (+40.0% max)** across all weapons, cloaks, and devotion bonuses combined.
  - Gilded Bow: +2000 BPS (+20%).
  - 360-Day Devotion: +1000 BPS (+10%).
  - Even with future gear expansions, code enforces: `if (goldBonusBps > 4000) goldBonusBps = 4000;`.
  - This is why companion animals do NOT have +15% gold buffs in the contract—it would pierce the macro-economic ceiling!

---

## 7. Progression & Leveling: "What Actually Levels Up?"

HoodQuest intentionally avoids runaway RPG level inflation (e.g. Level 1 to Level 99 with +5000% stats) because infinite stat inflation ruins 25-year game economies. Instead, progression is grounded in **biological time and craftsmanship**:

```text
┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
│           CHARACTER PROGRESSION (HQ)          │          COMPANION PROGRESSION (HQPET)        │
├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • Level: NO traditional arbitrary levels.     │ • Level: NO traditional arbitrary levels.     │
│ • Age: Effective Biological Age (Wakefulness) │ • Bond Rank: Ranks 1 to 5 based on XP.        │
│ • Devotion Milestones:                        │ • XP Source: +10 XP per daily forage.         │
│     - 30 Days Awake:  +2% Gold Bonus          │     - Rank 1: 0–299 XP (Novice)               │
│     - 90 Days Awake:  +4% Gold Bonus          │     - Rank 2: 300–899 XP (Trained)            │
│     - 180 Days Awake: +6% Gold Bonus          │     - Rank 3: 900–1799 XP (Loyal)             │
│     - 360 Days Awake: +10% Gold Bonus         │     - Rank 4: 1800–3649 XP (Devoted)          │
│ • Gear Loadout: Horizontal weapon choice      │     - Rank 5: 3650+ XP (Eternal Companion)    │
│   (Slots 0..5: Bow/Dagger/Staff, Cloak, Horn) │ • Output: Forages Yew & Iron for Blacksmith.  │
└───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

### 7.2 Awake vs. Sleeping Progression: The Permanent Rank Floor Architecture

To keep the game challenging yet compassionate, progression distinguishes between **Active Wakefulness** and **Slumber**:

```text
       [ RANK 1 FLOOR ] ──────▶ [ RANK 2 FLOOR ] ──────▶ [ RANK 3 FLOOR ]
             ▲                        ▲                        ▲
             │                        │                        │
       (Permanent Save)         (Permanent Save)         (Permanent Save)
             │                        │                        │
             └── In-progress climb    └── In-progress climb    └── In-progress climb
                 falls back only          falls back only          falls back only
                 to Rank 1 floor          to Rank 2 floor          to Rank 3 floor
```

1. **While AWAKE (Active Adventuring & Care):**
   * The hero and companion accumulate active biological wakefulness and XP toward the next rank milestone.
   * Day-by-day progress climbs smoothly between floors.
2. **While SLEEPING (Slumber / Absence):**
   * If a hero enters deep slumber mid-climb (e.g. 60% of the way between Rank 2 and Rank 3), sleeping can reset or pause the uncommitted in-between progress back to the **current rank floor (Rank 2)**.
   * **The Invariant Guarantee:** Sleeping **NEVER drops a character or companion below their achieved rank floor**. 
   * Once you reach Rank 2, you are Rank 2 forever. Once you cross 90 Days Awake (+4% Gold), you can sleep for a decade and you will *never* drop back to 30 Days or 0 Days.
3. **The Psychology:**
   * It creates an exciting incentive to push for the next milestone before taking a long break.
   * It completely eliminates "punishment depression"—players never log in after a hiatus to find their account ruined or their ranks stripped away. You always wake up safe on solid ground at your highest earned floor.

### 7.3 Conditioning & Devotion Streak: "The Rest & Rust" Graceful Decay Model
* **The Distinction:**
  - **Lifetime Biological Age:** Permanent on-chain record of total wakeful lifetime. **Never decays under any circumstance.**
  - **Active Devotion Conditioning:** Represents peak physical readiness and combat sharpness (+2% to +10% Gold Bonus).
* **The Rest & Rust Rule:**
  - While actively awake and maintained, conditioning days accumulate $+1$ per day toward Devotion Milestones (30, 90, 180, 360 days).
  - When the hero enters Slumber (inactivity without food/care), conditioning gracefully decays by $-1$ day for each day asleep ("gathering rust").
  - **Example:** An Outlaw who earned 90 days of conditioning and slumbers for 10 days wakes up with **80 days of conditioning**. Within 10 days of resuming active play, they are back to 90 days!
  - **Anti-Exploit Security:** Prevents a player from reaching 90 days once, going inactive for 2 years, and expecting to wake up with permanent, max-tier combat conditioning without shaking off the rust.
  - **Player Dignity:** A short vacation or busy work week only costs a few days of rust, easily brushed off upon returning to camp.




---

## 8. Secondary Market Gating: Native Bazaar vs. OpenSea

### 8.1 Native Camp Bazaar (`HoodQuestBazaar.sol`)
* Fully on-chain, zero external dependencies.
* Consults `canList(hoodId)`:
  - If `pendingGameplayCount != 0` (raid in flight) ➔ **Blocked.**
  - If `pendingUnequipCount != 0` (gear unequip timer running) ➔ **Blocked.**
  - If `pendingDebondMaturesAt != 0` (companion debond running) ➔ **Blocked.**
  - If `activeSolsticeCommitmentCount != 0` ➔ **Blocked.**
* **Result:** Zero race conditions or bait-and-switch trades possible in the Camp Bazaar.

### 8.2 External Marketplaces (OpenSea, Seaport, Blur)
* External platforms use off-chain EIP-712 order signatures.
* **Why Sellers Cannot Exploit Raids on External Markets:**
  1. Heist durations on Arbitrum Nitro L2 target `currentBlock + 2` (~0.5 seconds), so combat resolves before an external sale could confirm.
  2. If a seller transfers an Outlaw while a heist is pending, **rewards are delivered to the seller's wallet**, not the buyer.
  3. Transferring the Outlaw immediately cancels any pending unequip/debond timers and locks unequipping for 24 hours on the buyer.


---

## 9. Interactive NFT Metadata & OpenSea Iframe Architecture Pattern ("The Dual-Channel Tamagotchi Meta")

### 9.1 The Problem Statement & Industry Precedent
Traditional NFTs are static images or looping MP4s. Advanced interactive projects (such as Ape Hood on Robinhood Chain, Loot, and generative art on Art Blocks) leverage OpenSea's support for the `animation_url` metadata standard to embed interactive web applications directly inside marketplace item pages.

However, web3 game developers face a critical architectural dilemma:
1. **Can players play the game directly inside OpenSea?**
2. **How does the thumbnail interact with the interactive canvas?**
3. **How can players update traits or appearances with zero transaction fees?**
4. **Where should actual financial, combat, and vault transactions take place?**

This section codifies the canonical architecture, lessons learned, and reusable pattern for HoodQuest and future decentralized projects.

---

### 9.2 The Dual-Channel Standard: Thumbnail (`image`) vs. Interactive Player (`animation_url`)

OpenSea and major ERC-721 indexing engines implement a strict dual-channel display pipeline:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ERC-721 METADATA SCHEMA                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  {                                                                          │
│    "name": "Sherwood Outlaw #4",                                            │
│    "description": "Living on-chain Robin Hood pocket companion...",         │
│                                                                             │
│    "image": "data:image/svg+xml;base64,PHN2Zy...",                          │
│    ───────────────────────────────────────────────                          │
│    ▲ CHANNEL 1: The Static/Vector Thumbnail                                 │
│    │ • Displayed in: Search grids, collection galleries, activity feeds,    │
│    │   mobile marketplace apps, wallet previews, Discord/Twitter unfurls.   │
│    │ • Lightweight, instantly cacheable, zero script execution required.    │
│                                                                             │
│    "animation_url": "https://srhsoulja.github.io/hoodquest/?embed=4",       │
│    ──────────────────────────────────────────────────────────────────       │
│    ▲ CHANNEL 2: The Interactive HTML Canvas                                 │
│    │ • Mounted inside an <iframe> directly on the OpenSea item page.        │
│    │ • Executes HTML5 Canvas, WebAudio, CSS animations, click events.       │
│    │ • Features native marketplace toggle (Switch between 2D & Interactive).│
│  }                                                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Why Both Are Mandatory:
* If you **only** provide `animation_url` without `image`: The collection grid and mobile wallets display a broken or blank thumbnail.
* If you **only** provide `image` without `animation_url`: The NFT is stuck as a flat picture and cannot be played with or animated on OpenSea.
* **The Best Practice:** `image` serves the crisp, deterministic on-chain character portrait (`generateSVG()`), while `animation_url` delivers the living campfire diorama.

---

### 9.3 Division of Labor: Pocket Tamagotchi (OpenSea) vs. The Cartridge Hub

#### The Core Insight: "Leave the Real Stuff to the Cart"
OpenSea embeds `animation_url` using a strictly sandboxed iframe:
```html
<iframe 
  allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
  sandbox="allow-scripts" 
  src="...">
</iframe>
```

#### Browser Security Constraints of the OpenSea Iframe:
1. **`allow-scripts` is granted:** JavaScript executes, Canvas renders, particle engines run, and WebAudio sounds play upon user interaction.
2. **`allow-same-origin` is intentionally OMITTED:** For marketplace security, the browser isolates the iframe. This means **browser wallet extensions (MetaMask, Coinbase Wallet `window.ethereum`) are blocked by the browser inside the iframe**.
3. **Wallet Connect in Iframes:** While WalletConnect modal popups can technically trigger deep-links, browser popup blockers and iframe security policies make signing high-stakes gameplay transactions inside an OpenSea iframe clunky and error-prone.

#### The Canonical Separation of Responsibilities:

```text
┌──────────────────────────────────────────────┬──────────────────────────────────────────────┐
│       OPENSEA IFRAME (Pocket Diorama)        │           THE CARTRIDGE HUB (Game Engine)    │
├──────────────────────────────────────────────┼──────────────────────────────────────────────┤
│ • Role: Interactive Showcase & Tamagotchi    │ • Role: Authoritative Execution Engine       │
│ • Living campfire ambient particles & smoke  │ • Full Web3 Wallet Connection (MetaMask/WC)  │
│ • Day/night lighting cycles                  │ • Royal Carriage Ambush & Combat Execution   │
│ • Bonded companion resting beside hero       │ • Daily Care Proof-of-Life Signing           │
│ • Clickable actions (stoke fire, pet treats) │ • Soulbound Yew & Iron Crafting / Forging    │
│ • Interactive cosmetic / wardrobe preview    │ • Camp Bazaar Escrow Trading & Listings      │
│ • Live stats inspection (Age, Devotion, Rank)│ • High-stakes vault raids & treasury payouts │
│ • [🌲 Enter Sherwood / Launch Hub ↗] Portal   │ • Native full-screen cartridge console       │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

---

### 9.4 Gasless Trait & Appearance Updating (The Industry Metas)

Projects like Based Apes / Ape Hood popularized letting users update their character's appearance and traits with **zero transaction fees**. Our reverse-engineering of their production code identified the two distinct implementations:

#### Pattern A: The Centralized Off-Chain API (Ape Hood Method)
1. The contract `tokenURI` points to a hosted server: `https://api.project.com/metadata/{id}`.
2. In the wardrobe dApp, the user selects new clothes and clicks save.
3. The frontend calls `POST /api/save?token={id}&clothes={item}`.
4. The server database updates. When OpenSea crawls the metadata, the API returns the new attributes and composited PNG.
5. **Tradeoff:** Zero gas for players, but **zero blockchain permanence**. If the centralized server or domain expires, the NFT and its metadata vanish.

#### Pattern B: Gasless On-Chain Meta-Transactions + EIP-4906 (The HoodQuest Sovereign Method)
To achieve zero-gas styling while preserving **100% blockchain decentralization and permanence**:
1. **The EIP-712 Permit:** The player selects their earned cloak or bow and signs a typed message in their wallet (`EquipPermit(tokenId, gearId, nonce, deadline)`). Signing a message has **$0 gas cost**.
2. **The Gasless Relayer (Paymaster):** The game's relayer collects the signature and submits it to Robinhood Chain (Arbitrum Nitro L2 gas is ~$0.0005, easily sponsored by community rebate reserves).
3. **EIP-4906 Invalidation Event:** The contract verifies the signature, updates the equipped slot, and emits:
   ```solidity
   event MetadataUpdate(uint256 _tokenId);
   ```
4. **OpenSea Cache Sync:** OpenSea’s indexing daemon listens for `MetadataUpdate(tokenId)`. Upon receipt, OpenSea automatically invalidates its cached traits and re-indexes the Outlaw’s on-chain SVG and trait chips—**updating the listed traits on OpenSea with zero gas paid by the player!**

---

### 9.5 Reusable Implementation Checklist for Future Projects

When building interactive on-chain NFTs with marketplace support:
* [ ] **Metadata Dual-Field:** Ensure `tokenURI` returns both `image` (valid SVG or PNG data URI) and `animation_url` (HTML data URI or HTTPS URL).
* [ ] **Responsive Viewport:** Set `<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">` so the canvas scales smoothly from mobile cards (300px) to desktop modals (800px).
* [ ] **Autoplay Audio Policy:** Browsers block audio in iframes until the user interacts. Gate all sound effects and ambient lutes behind an explicit click event (`canvas.addEventListener('click', initAudio)`).
* [ ] **Deep-Link Escape Hatch:** Always include a prominent top/bottom anchor button (`target="_blank"`) that allows visitors to exit the sandboxed iframe and enter the full game hub.
* [ ] **EIP-4906 Support:** Implement the `IERC4906` interface (`0x49064906`) and emit `MetadataUpdate(tokenId)` whenever on-chain or sponsored changes occur so marketplaces never show stale metadata.

---

## 10. SOP: Making Changes & Preventing Regression

Whenever proposing or implementing changes to HoodQuest:
1. **Check Against HOODQUEST_MASTER_BLUEPRINT.md:** Does this change contradict any protocol-frozen invariant (constants, supply modes, split caps, 25-year pillars)?
2. **Respect the Three-Tier Architecture:**
   - Never put mutable game rules or raid math into Tier 1 (`HoodQuest.sol`, `HoodQuestTreasures.sol`, `HoodQuestCompanions.sol`).
   - Put all gameplay logic, raid formulas, and seasonal events into Tier 2 (`HoodQuestRaids.sol`).
   - Consoles and frontends (Tier 3) query the World Authority dynamically.
3. **Verify Bit-for-Bit Cartridge Invariance:**
   - In `prototype/index.html`, do not alter bytecode or logic prior to line 5416.
   - Always run `python3 build_cartridge.py` to confirm decompression and SSTORE2 chunk parity before committing.
4. **Log the Decision Here:** Document the rationale in this file before deploying to testnet or mainnet.

