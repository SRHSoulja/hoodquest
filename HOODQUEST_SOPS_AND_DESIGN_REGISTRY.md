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

## 9. SOP: Making Changes & Preventing Regression

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
