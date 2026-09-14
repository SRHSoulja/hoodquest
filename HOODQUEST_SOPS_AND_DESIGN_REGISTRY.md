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

## 5. SOP: Making Changes & Preventing Regression

Whenever proposing or implementing changes to HoodQuest:
1. **Check Against `HOODQUEST_MASTER_BLUEPRINT.md`:** Does this change contradict any protocol-frozen invariant (constants, supply modes, split caps, 25-year pillars)?
2. **Respect the Three-Tier Architecture:**
   - Never put mutable game rules or raid math into Tier 1 (`HoodQuest.sol`, `HoodQuestTreasures.sol`, `HoodQuestCompanions.sol`).
   - Put all gameplay logic, raid formulas, and seasonal events into Tier 2 (`HoodQuestRaids.sol`).
   - Consoles and frontends (Tier 3) query the World Authority dynamically.
3. **Verify Bit-for-Bit Cartridge Invariance:**
   - In `prototype/index.html`, do not alter bytecode or logic prior to line 5416.
   - Always run `python3 build_cartridge.py` to confirm decompression and SSTORE2 chunk parity before committing.
4. **Log the Decision Here:** Document the rationale in this file before deploying to testnet or mainnet.
