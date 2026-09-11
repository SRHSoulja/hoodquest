import os
import sys

def build_section_0():
    return r"""# HoodQuest (HQ): Production System Specification (Protocol Frozen V1.0-RC2)

A mathematically closed, executable smart contract specification for **HoodQuest (HQ)**, a 100% on-chain living companion RPG with zero backend servers, indexers, or relayers, deployed natively on **Robinhood Chain (Testnet Chain ID 46630, Mainnet Chain ID 4663)**.

- **Official Brand:** **HoodQuest**
- **Shorthand / Ticker:** **HQ**
- **Testnet Subdomain:** `rhtestnethq.gmgnrepeat.com`
- **Future Mainnet Subdomain:** `hq.gmgnrepeat.com`
- **Specification Release:** **Protocol Frozen V1.0-RC2 (Specification Closure Release)**
- **Strict Network Boundary:** Testing and deployment are strictly restricted to **Robinhood Testnet (Chain ID 46630)** and local Foundry test environments. Mainnet (Chain ID 4663) remains locked until full audit cycle completion.

---

## Table of Contents
1. [Core Vision & 25-Year Pillars](#1-core-vision--25-year-pillars)
2. [Smart Contract Topology & Security Architecture](#2-smart-contract-topology--security-architecture)
3. [The Calibrated 25-Year Economic Engine & Heist State Machine](#3-the-calibrated-25-year-economic-engine--heist-state-machine)
4. [The Armory Escrow Vault & Bazaar Custody Engine](#4-the-armory-escrow-vault--bazaar-custody-engine)
5. [Anti-Power-Creep Weapon Matrix & The Blacksmith](#5-anti-power-creep-weapon-matrix--the-blacksmith)
6. [Mother Meg's Rescue Post & Companion Sidecars](#6-mother-megs-rescue-post--companion-sidecars)
7. [The Upkeep, Slumber & Calibrated Devotion System](#7-the-upkeep-slumber--calibrated-devotion-system)
8. [Gas-Free On-Chain Minigames & Artisan Vector Art Pipeline](#8-gas-free-on-chain-minigames--artisan-vector-art-pipeline)
9. [The Sherwood Astronomical Calendar & World Events Engine](#9-the-sherwood-astronomical-calendar--world-events-engine)
10. [Bounded-Emission Governance & Expansion Blueprint](#10-bounded-emission-governance--expansion-blueprint)
11. [Master Pre-Flight Audit & Verification Lifecycle Matrix](#11-master-pre-flight-audit--verification-lifecycle-matrix)
12. [Mainnet Acceptance Test & Invariant Specification](#12-mainnet-acceptance-test--invariant-specification)
13. [Normative Requirements Registry](#13-normative-requirements-registry)

---
"""

def build_section_1():
    return r"""## 1. Core Vision & 25-Year Pillars

```mermaid
flowchart TD
    subgraph Pillars ["Core System Pillars"]
        P1["Living Pocket Companion<br>25 Active Years of Living Devotion"]
        P2["Pure On-Chain SVG<br>Solidity Direct Rendering & EIP-4906"]
        P3["Deflationary Gold Sink Engine<br>Rebate Reserve + Net 75% Permanent Burn"]
        P4["Armory Escrow Vault<br>Aggregate ERC-1155 Custody & Bazaar Escrow"]
        P5["Anti-Power-Creep Covenant<br>Stat Ceilings & Split 750/250 Caps"]
        P6["Zero-Server World Engine<br>360+5 Solstice Calendar & ActionRequest Engine"]
        P7["Bounded-Emission Governance<br>Core Owns Limits; Timelocked Modules"]
    end
```

1. **"25 Years" Means 25 Years of Active Devotion:** Biological evolution is driven strictly by **effective wakefulness**. Slumber pauses the biological aging clock ($0 gas during sleep). For average players taking real-world breaks, reaching Legend status spans **35 to 50+ real-world calendar years**, creating a multi-generational digital heirloom.
2. **Decoupled Hero Age vs. Sherwood World Calendar:** Hero Biological Age (advancing only when cared for and awake) is strictly decoupled from the perpetual **Sherwood World Calendar** (an autonomous 365-day astronomical cycle of 12 thirty-day months plus 5 intercalary Solstice days running perpetually).
3. **100% On-Chain Autonomy:** Zero centralized servers, zero indexer dependencies, zero gas relayers. All visuals, stats, encounters, and loot rolls live directly in Solidity EVM bytecode.
4. **Capped Macro Economy:** Governed by an immutable maximum token supply (`MAX_HOOD_SUPPLY = 10,000`), token IDs strictly start at 1, and no admin mint or un-capped emission paths exist.
5. **Anti-Power-Creep Guarantee:** Early Genesis gear (2026) is never rendered obsolete. Statutory stat ceilings, split drop/forge caps, and horizontal gear selection protect player investments forever.
6. **Bounded-Emission Governance:** The developer has zero admin-mint capabilities. All expansions use a 48-hour public on-chain timelock and cannot exceed strict daily emission budgets.
7. **Identity-Bound Temporal Tracking:** All daily allowances, stamina limits, rations, and cooldowns are permanently bound to the **NFT Token ID**, never resetting upon wallet transfers.

---
"""

def build_section_2():
    return r"""## 2. Smart Contract Topology & Security Architecture

The protocol is divided into specialized contracts to strictly respect Ethereum's 24,576-byte bytecode cap (EIP-170), isolate economic risk, and allow presentation upgrades while keeping economic invariants immutable:

```mermaid
graph TD
    A["HoodQuest.sol (ERC-721 + Enumerable + EIP-4906 Core)<br>Identity, Age, Stamina Counters, Armory Escrow, Canonical Gating"] 
    W["HoodQuestWorldState.sol (Persistent World Registry)<br>Sherwood Calendar, Census, Boss Thresholds, Castle Progress, Leaderboards"]
    B["HoodQuestTreasures.sol (ERC-1155Supply)<br>Royal Gold, Gear, Blacksmith, Rebate Reserve, Expansion Registry"]
    C["HoodQuestCompanions.sol (ERC-721 + Enumerable)<br>10,000 Pets, Foraging, Bond Ranks"]
    D["HoodQuestRaids.sol (Replaceable Combat & Action Engine)<br>Heists, Monthly Raids, Tax Train, Jubilees, Solstice"]
    E["HoodQuestBazaar.sol (Native Camp Bazaar)<br>On-Chain Gold Custody & Loadout Freeze"]
    R["HoodQuestRenderer.sol (Replaceable Engine)<br>Procedural Vector Art & Metadata Strings"]

    A <--> B
    A <--> C
    A <--> D
    A <--> E
    B <--> D
    C <--> D
    B <--> E
    D <--> W
    A -.->|assembly staticcall| R
```

### Contract Responsibilities:

- **`HoodQuest.sol` (ERC-721 + `ERC721Enumerable` + EIP-4906 Core + Receivers):**
  - Symbol: **`HQ`** | Maximum Supply: **`MAX_HOOD_SUPPLY = 10,000`** (Immutable constant).
  - **Receiver Support (HQ-CORE-003):** Inherits OpenZeppelin `ERC1155Holder` and implements `IERC721Receiver` to securely hold escrowed armory equipment and bonded companions:
    ```solidity
    function onERC721Received(address, address, uint256, bytes calldata) external pure override returns (bytes4) {
        return this.onERC721Received.selector;
    }
    ```
  - **Token ID Range:** Strictly `1` through `10,000` (`0` is the unassigned/sentinel value).
  - **Immutable Constructor Deployment Manifest:**
    ```solidity
    constructor(
        uint256 mintPriceWei_,
        address proceedsRecipient_,
        uint256 genesisTime_
    ) {
        require(proceedsRecipient_ != address(0), "Invalid recipient");
        require(genesisTime_ <= block.timestamp, "Genesis in future");
        MINT_PRICE_WEI = mintPriceWei_;
        PROCEEDS_RECIPIENT = proceedsRecipient_;
        GENESIS_TIME = genesisTime_;
    }
    ```
  - **Public Mint Function & Fresh-Hood Initialization:**
    ```solidity
    function mintHoods(uint8 count) external payable nonReentrant {
        require(count >= 1 && count <= 5, "Count must be 1..5");
        require(totalHoodsMinted + count <= MAX_HOOD_SUPPLY, "Exceeds max supply");
        require(msg.value == MINT_PRICE_WEI * count, "Exact payment required");
        
        for (uint8 i = 0; i < count; i++) {
            uint256 id = ++totalHoodsMinted;
            mintTimestamp[id] = uint64(block.timestamp);
            lastCareTimestamp[id] = uint64(block.timestamp);
            lastCareDay[id] = currentUtcDay() - 1; // Allows immediate first-day care
            delegateEpoch[id] = 1;
            rationsUntil[id] = uint64(block.timestamp + 7 days); // 7 days starter rations as state
            slumberAccountedUntil[id] = uint64(block.timestamp);
            seedTargetBlock[id] = ArbSys(0x64).arbBlockNumber() + 2;
            _safeMint(msg.sender, id);
        }
    }

    function withdrawMintProceeds() external nonReentrant {
        uint256 balance = address(this).balance;
        require(balance > 0, "No proceeds");
        (bool success, ) = PROCEEDS_RECIPIENT.call{value: balance}("");
        require(success, "Proceeds transfer failed");
    }
    ```
  - **Delayed Seed Assignment & Deterministic Fallback:**
    After `seedTargetBlock` passes, anyone may call `finalizeHeroSeed(tokenId)`:
    ```solidity
    function finalizeHeroSeed(uint256 tokenId) external {
        require(heroSeed[tokenId] == bytes32(0), "Already finalized");
        uint256 target = seedTargetBlock[tokenId];
        require(target > 0, "Not minted");
        uint256 current = ArbSys(0x64).arbBlockNumber();
        require(current > target, "Target not reached");
        if (current <= target + 256) {
            heroSeed[tokenId] = keccak256(abi.encode(
                ArbSys(0x64).arbBlockHash(target),
                tokenId,
                address(this),
                block.chainid
            ));
        } else {
            // Fixed non-random fallback: assigns standard genesis recruit traits
            heroSeed[tokenId] = keccak256(abi.encode("STANDARD_GENESIS", tokenId, GENESIS_TIME));
            standardGenesis[tokenId] = true;
        }
        emit HeroSeedFinalized(tokenId, heroSeed[tokenId]);
    }
    ```
    **Economic Gameplay Requirement:** All heists, Castle maneuvers, Boss attacks, and Genesis adoptions strictly require `heroSeed[hoodId] != bytes32(0)`.
  - **Canonical Core Gating Counters & Pre-Sale Gate (`canList`) (HQ-CORE-004, HQ-CORE-005):**
    To ensure complete upgrade safety across Raid engine replacements, all token-level activity gates live authoritatively in `HoodQuest.sol`:
    ```solidity
    mapping(uint256 => uint32) public pendingGameplayCount;
    mapping(uint256 => uint32) public pendingEventEntitlementCount;
    mapping(uint256 => uint32) public pendingHeistRewardCount;
    mapping(uint256 => bool) public activeSolsticeLock;

    function incrementPendingGameplay(uint256 hoodId, uint32 count) external onlyAuthorizedEngine {
        pendingGameplayCount[hoodId] += count;
    }
    function decrementPendingGameplay(uint256 hoodId, uint32 count) external onlyAuthorizedEngine {
        require(pendingGameplayCount[hoodId] >= count, "Gameplay counter underflow");
        pendingGameplayCount[hoodId] -= count;
    }

    function incrementPendingEventEntitlement(uint256 hoodId) external onlyAuthorizedEngine {
        pendingEventEntitlementCount[hoodId]++;
    }
    function decrementPendingEventEntitlement(uint256 hoodId) external onlyAuthorizedEngine {
        require(pendingEventEntitlementCount[hoodId] > 0, "Event entitlement underflow");
        pendingEventEntitlementCount[hoodId]--;
    }

    function incrementPendingHeistReward(uint256 hoodId) external onlyAuthorizedEngine {
        pendingHeistRewardCount[hoodId]++;
    }
    function decrementPendingHeistReward(uint256 hoodId) external onlyAuthorizedEngine {
        require(pendingHeistRewardCount[hoodId] > 0, "Heist reward underflow");
        pendingHeistRewardCount[hoodId]--;
    }

    function setSolsticeLock(uint256 hoodId, bool locked) external onlyAuthorizedEngine {
        activeSolsticeLock[hoodId] = locked;
    }

    function canList(uint256 hoodId) public view returns (bool allowed, uint256 reasonFlags) {
        if (pendingGameplayCount[hoodId] > 0) reasonFlags |= 1;
        if (pendingUnequipCount[hoodId] > 0) reasonFlags |= 2;
        if (pendingDebondMaturesAt[hoodId] > 0) reasonFlags |= 4;
        if (activeSolsticeLock[hoodId]) reasonFlags |= 8;
        if (pendingEventEntitlementCount[hoodId] > 0) reasonFlags |= 16;
        if (pendingHeistRewardCount[hoodId] > 0) reasonFlags |= 32;
        allowed = (reasonFlags == 0);
    }
    ```
  - **Bazaar Transfer-Mode Handshake & Hook Wiping (HQ-CORE-006):**
    ```solidity
    enum BazaarTransferMode { NONE, LISTING_DEPOSIT, CANCEL_WITHDRAWAL, SALE_PURCHASE }
    BazaarTransferMode public bazaarTransferMode;

    function setBazaarTransferMode(BazaarTransferMode mode) external onlyBazaar {
        bazaarTransferMode = mode;
    }

    function _update(address to, uint256 tokenId, address auth) internal override returns (address from) {
        from = super._update(to, tokenId, auth);
        
        if (to == address(bazaarContract)) {
            require(bazaarContract.expectedDeposit(tokenId) == from, "Unsolicited Bazaar deposit prohibited");
        }
        
        if (from != address(0) && to != address(0) && from != to) {
            for (uint8 s = 0; s < 7; s++) {
                delete pendingUnequip[tokenId][s];
            }
            pendingUnequipCount[tokenId] = 0;
            delete pendingDebondMaturesAt[tokenId];
            
            if (msg.sender == address(bazaarContract)) {
                if (bazaarTransferMode == BazaarTransferMode.CANCEL_WITHDRAWAL) {
                    // Cancellation returns to original seller: no lock, preserve delegateEpoch
                } else if (bazaarTransferMode == BazaarTransferMode.SALE_PURCHASE) {
                    postTransferUnequipLockedUntil[tokenId] = uint64(block.timestamp + 24 hours);
                    delegateEpoch[tokenId]++;
                }
            } else {
                // External wallet-to-wallet transfer: enforce 24h buyer lock and wipe delegates
                postTransferUnequipLockedUntil[tokenId] = uint64(block.timestamp + 24 hours);
                delegateEpoch[tokenId]++;
            }
        }
    }
    ```
  - **Stamina & Temporal State Authority:** The core permanently owns and tracks:
    - `baseHeistsUsed[tokenId]` (max 5/day)
    - `bonusHeistsUsed[tokenId]` (max 5/day via Elixir)
    - `lastHeistDay[tokenId]`
    - `lastCareDay[tokenId]`
    - `lastElixirDay[tokenId]`
    - `pendingNormalHeist[tokenId]` (boolean: strictly at most 1 pending heist batch per Hood)
    - `effectiveBiologicalAge[tokenId]`
    - Derived UTC day helper:
      ```solidity
      function currentUtcDay() public view returns (uint32) {
          return uint32(block.timestamp / 1 days);
      }
      ```
  - **O(1) Delegate Wiping via Delegation Epochs (HQ-CORE-007):**
    ```solidity
    mapping(uint256 => uint64) public delegateEpoch;
    mapping(uint256 => mapping(address => uint64)) public delegateGrantedEpoch;

    function isGameDelegate(uint256 hoodId, address operator) public view returns (bool) {
        return delegateGrantedEpoch[hoodId][operator] == delegateEpoch[hoodId] && delegateEpoch[hoodId] > 0;
    }

    function setGameDelegate(uint256 hoodId, address operator, bool authorized) external {
        require(ownerOf(hoodId) == msg.sender, "Not owner");
        if (authorized) {
            delegateGrantedEpoch[hoodId][operator] = delegateEpoch[hoodId];
        } else {
            delegateGrantedEpoch[hoodId][operator] = 0;
        }
    }
    ```
  - **Delegate Scope & Item Spending (HQ-CORE-008):**
    - Authorized delegates may call: `dailyCare`, `feed`, companion `soloForage`, `requestHeistBatch`, `resolveHeist`, `claimHeistRewards` (strictly to `ownerOf(hoodId)`), and `requestActionEvent`.
    - **Caller Inventory Rule:** When delegates call `feed(hoodId)` or `useElixir(hoodId)`, items are burned **strictly from `msg.sender` (the delegate's own balance)**. Delegates can never spend or burn inventory from the Hood owner.
    - Delegates are **strictly forbidden** from: listing on Bazaar, transferring tokens, equipping items, bonding pets, initiating/finalizing unequips or debonds, and withdrawing assets.
  - **Emergency Guardian Pause State Machine:**
    ```solidity
    uint64 public guardianPauseUntil;
    uint64 public lastGuardianPauseStarted;

    function economicActionsPaused() public view returns (bool) {
        return block.timestamp < guardianPauseUntil;
    }

    function triggerGuardianPause() external onlyGuardian {
        require(block.timestamp >= guardianPauseUntil, "Already paused");
        require(block.timestamp >= lastGuardianPauseStarted + 7 days, "Pause cooldown active");
        guardianPauseUntil = uint64(block.timestamp + 72 hours);
        lastGuardianPauseStarted = uint64(block.timestamp);
        emit EmergencyPauseTriggered(guardianPauseUntil);
    }
    ```
  - **Presentation Upgradeability & Returndata-Protected Fallback with Strict ABI Padding (HQ-GOV-005):**
    ```solidity
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);
        address rend = address(renderer);
        if (rend != address(0)) {
            bytes memory callData = abi.encodeWithSelector(IRenderer.tokenURI.selector, tokenId);
            uint256 maxLen = 100_000;
            bool ok;
            uint256 size;
            
            assembly {
                ok := staticcall(2000000, rend, add(callData, 0x20), mload(callData), 0, 0)
                size := returndatasize()
            }
            
            if (ok && size >= 64 && size <= maxLen) {
                bytes memory data = new bytes(size);
                assembly {
                    returndatacopy(add(data, 0x20), 0, size)
                }
                uint256 offset;
                uint256 strLen;
                assembly {
                    offset := mload(add(data, 0x20))
                    strLen := mload(add(data, 0x40))
                }
                uint256 padded = (strLen + 31) & ~uint256(31);
                if (offset == 32 && 64 + padded <= size) {
                    return abi.decode(data, (string));
                }
            }
        }
        return _fallbackTokenURI(tokenId);
    }
    ```

- **`HoodQuestWorldState.sol` (Persistent Canonical World Registry - HQ-EVT-002):**
  - Holds all persistent world progress across Raid engine replacements:
    - `monthlyActiveHoodCount[monthEpoch]`
    - `taxTrainCumulativeGoldBurnSnapshot`
    - `nextTaxTrainBossThreshold`
    - `bossCooldownEndsAt`
    - `castleBreachPoints[eventId]`, `castleBreached[eventId]`
    - `jubileeTopHood[eventId][5]`, `jubileeTopScore[eventId][5]`
    - `solsticeRenown[eventId][hoodId]`
    - `hoodContribution[eventId][hoodId]`, `totalContribution[eventId]`
    - `eventEntitlementOpen[eventId][hoodId]`
    - `events[eventId]`
  - Governed by `onlyAuthorizedEngine` access, guaranteeing that retiring Raid Engine V1 and launching V2 never resets the 25-year living world timeline or fragmented boss thresholds.

- **`HoodQuestTreasures.sol` (ERC-1155Supply Accounting Authority):**
  - Inherits OpenZeppelin `ERC1155Supply` for authoritative tracking of `totalSupply(id)`.
  - **Explicit Three-Tier Engine Permissions (HQ-TREAS-004):**
    ```solidity
    mapping(address => bool) public activeRaidEngine;    // May request heists, consume stamina, create events
    mapping(address => bool) public resolverApproved;     // May resolve existing requests & reserve drops/trophies
    mapping(address => bool) public settlementApproved;   // May settle existing reward claims & event liabilities
    ```
  - **Multi-Unit Drop Reservations (HQ-TREAS-006):**
    ```solidity
    function reserveItem(
        uint256 itemId,
        MintSource source,
        uint256 requestedAmount
    ) external onlyResolver returns (uint256 reservedAmount) {
        if (requestedAmount == 0) return 0;
        
        if (itemId == GILDED_BOW) {
            require(source == MintSource.DROP, "Gilded Bow reserved strictly from drops");
            uint256 dropAvail = 0;
            if (droppedGildedBows + dropReservedGildedBows < 250) {
                dropAvail = 250 - (droppedGildedBows + dropReservedGildedBows);
            }
            uint256 totalAvail = 0;
            if (lifetimeMinted[itemId] + reservedUnclaimed[itemId] < 1000) {
                totalAvail = 1000 - (lifetimeMinted[itemId] + reservedUnclaimed[itemId]);
            }
            uint256 avail = dropAvail < totalAvail ? dropAvail : totalAvail;
            reservedAmount = requestedAmount <= avail ? requestedAmount : avail;
            dropReservedGildedBows += reservedAmount;
            reservedUnclaimed[itemId] += reservedAmount;
            return reservedAmount;
        }
        
        SupplyMode mode = itemSupplyMode[itemId];
        uint256 cap = itemLifetimeCap[itemId];
        if (mode == SupplyMode.UNCAPPED) return requestedAmount;
        
        if (mode == SupplyMode.MAX_CIRCULATING) {
            uint256 current = totalSupply(itemId) + reservedUnclaimed[itemId];
            if (current >= cap) return 0;
            uint256 avail = cap - current;
            reservedAmount = requestedAmount <= avail ? requestedAmount : avail;
            reservedUnclaimed[itemId] += reservedAmount;
            return reservedAmount;
        }
        
        if (mode == SupplyMode.MAX_LIFETIME) {
            uint256 current = lifetimeMinted[itemId] + reservedUnclaimed[itemId];
            if (current >= cap) return 0;
            uint256 avail = cap - current;
            reservedAmount = requestedAmount <= avail ? requestedAmount : avail;
            reservedUnclaimed[itemId] += reservedAmount;
            return reservedAmount;
        }
        
        return 0;
    }
    ```
  - **Event Gold & Trophy Accounting Authority (HQ-TREAS-007):**
    ```solidity
    mapping(address => mapping(uint256 => uint256)) public eventGoldReserved;
    mapping(address => mapping(uint256 => uint256)) public eventGoldMinted;
    mapping(address => mapping(uint256 => mapping(uint256 => uint256))) public eventTrophyReserved;
    mapping(uint256 => uint256) public forfeitedGrails;

    function reserveEventBudget(uint256 eventId, uint256 cap) external onlyActiveRaid returns (uint256 budget) {
        budget = cap < rebateReserve ? cap : rebateReserve;
        rebateReserve -= budget;
        eventGoldReserved[msg.sender][eventId] = budget;
        emit EventBudgetReserved(eventId, budget);
    }

    function mintReservedEventGold(address recipient, uint256 eventId, uint256 amount) external onlySettlementApproved nonReentrant {
        require(eventGoldMinted[msg.sender][eventId] + amount <= eventGoldReserved[msg.sender][eventId], "Exceeds reserved budget");
        eventGoldMinted[msg.sender][eventId] += amount;
        _mint(recipient, 1, amount, "");
    }

    function refundEventBudget(uint256 eventId, uint256 amount) external onlySettlementApproved {
        require(eventGoldMinted[msg.sender][eventId] + amount <= eventGoldReserved[msg.sender][eventId], "Refund exceeds reserved");
        eventGoldReserved[msg.sender][eventId] -= amount;
        rebateReserve += amount;
        emit EventBudgetRefunded(eventId, amount);
    }

    function reserveEventTrophy(uint256 eventId, uint256 itemId, uint256 quantity) external onlyActiveRaid {
        require(lifetimeMinted[itemId] + reservedUnclaimed[itemId] + forfeitedGrails[itemId] + quantity <= 25, "Grail cap exceeded");
        reservedUnclaimed[itemId] += quantity;
        eventTrophyReserved[msg.sender][eventId][itemId] += quantity;
        emit EventTrophyReserved(msg.sender, eventId, itemId, quantity);
    }

    function mintReservedTrophy(uint256 eventId, address recipient, uint256 itemId) external onlySettlementApproved nonReentrant {
        require(eventTrophyReserved[msg.sender][eventId][itemId] > 0, "No event trophy reservation");
        require(reservedUnclaimed[itemId] > 0, "No global reservation");
        eventTrophyReserved[msg.sender][eventId][itemId]--;
        reservedUnclaimed[itemId]--;
        lifetimeMinted[itemId]++;
        _mint(recipient, itemId, 1, "");
    }

    function forfeitReservedTrophy(uint256 eventId, uint256 itemId) external onlySettlementApproved {
        require(eventTrophyReserved[msg.sender][eventId][itemId] > 0, "No event trophy reservation");
        require(reservedUnclaimed[itemId] > 0, "No global reservation");
        eventTrophyReserved[msg.sender][eventId][itemId]--;
        reservedUnclaimed[itemId]--;
        forfeitedGrails[itemId]++;
        emit TrophyPermanentlyForfeited(eventId, itemId);
    }
    ```
  - **Enforceable Soulbound Proof-of-Play (Yew #16 & Iron #17):**
    ```solidity
    function _update(address from, address to, uint256[] memory ids, uint256[] memory values) internal override {
        for (uint256 i = 0; i < ids.length; i++) {
            if (ids[i] == YEW || ids[i] == IRON) {
                require(from == address(0) || to == address(0), "Soulbound: non-transferable");
            }
        }
        super._update(from, to, ids, values);
    }
    ```
  - **Unified Global `rebateReserve` with Fractional Carry:**
    ```solidity
    function _burnGold(address from, uint256 amount) internal {
        _burn(from, 1, amount);
        cumulativeGoldBurned += amount;
        uint256 scaled = amount * 2500 + rebateCarryBps;
        uint256 credit = scaled / 10_000;
        rebateCarryBps = uint16(scaled % 10_000);
        rebateReserve += credit;
    }
    ```

- **`HoodQuestCompanions.sol` (ERC-721 + `ERC721Enumerable`):**
  - Maximum Supply: **`MAX_COMPANION_SUPPLY = 10,000`** (4,000 Camp Hounds, 3,000 Hunting Falcons, 3,000 Barn Owls).
  - **Genesis Adoption Guard (1 Genesis Adoption per Hood Lifetime):**
    ```solidity
    mapping(uint256 => bool) public genesisAdoptionUsed;
    uint256 public nextHoundId = 1;     // 1..4000
    uint256 public nextFalconId = 4001; // 4001..7000
    uint256 public nextOwlId = 7001;    // 7001..10000

    function adoptGenesisPet(uint256 hoodId, uint8 species) external returns (uint256 petId) {
        require(hoodContract.ownerOf(hoodId) == msg.sender, "Not Hood owner");
        require(!genesisAdoptionUsed[hoodId], "Genesis pet already adopted for this Hood");
        require(!hoodContract.economicActionsPaused(), "Economic actions paused");
        require(hoodContract.heroSeed(hoodId) != bytes32(0), "Hero seed not finalized");
        
        genesisAdoptionUsed[hoodId] = true;
        
        if (species == 0) {
            require(nextHoundId <= 4000, "Hounds exhausted");
            petId = nextHoundId++;
            treasuresContract.burnAdoptionGold(msg.sender, 20);
        } else if (species == 1) {
            require(nextFalconId <= 7000, "Falcons exhausted");
            petId = nextFalconId++;
            treasuresContract.burnAdoptionGold(msg.sender, 30);
        } else if (species == 2) {
            require(nextOwlId <= 10000, "Owls exhausted");
            petId = nextOwlId++;
            treasuresContract.burnAdoptionGold(msg.sender, 40);
        } else {
            revert("Invalid species");
        }
        
        petSeed[petId] = keccak256(abi.encode(
            hoodContract.heroSeed(hoodId),
            petId,
            species,
            address(this),
            block.chainid
        ));
        
        _safeMint(msg.sender, petId);
        emit CompanionAdopted(hoodId, petId, species);
    }
    ```

- **`HoodQuestRaids.sol` (Combat & Action Engine):**
  - Executes daily batch heists, Monthly Castle Vault Infiltrations, Tax Train World Bosses, 5-Year Jubilees, and the Grand Solstice Vault Heist.
  - **Multi-Counter Retirement Protocol (HQ-GOV-004):**
    ```solidity
    mapping(address => uint256) public pendingRequestsByEngine;
    mapping(address => uint256) public outstandingRewardClaimsByEngine;
    mapping(address => uint256) public outstandingEventLiabilitiesByEngine;
    ```
    A retired engine loses request creation authority immediately; loses new reservation authority once `pendingRequestsByEngine == 0`; and retains settlement authority until all outstanding claims and event liabilities reach zero.

- **`HoodQuestBazaar.sol` (Native Camp Bazaar):**
  - Atomic fee burn + proceeds custody escrow. Zero Gold minting authority. Implements `IERC1155Receiver`.

---
"""

def build_section_3():
    return r"""## 3. The Calibrated 25-Year Economic Engine & Heist State Machine

```mermaid
flowchart LR
    A["00:00 UTC Reset<br>5 Base Heists (Core-Bound)"] --> B["Carriage Ambush<br>(Snapshot + Delayed L2 Entropy)"]
    B -->|"Base Roll: 1-3 Gold"| C["🪙 Royal Gold Sovereigns<br>(Fixed-point starvation + bonus carry)"]
    B -->|"25% Quest Drop"| D1["🪵 Sherwood Yew (Soulbound)"]
    B -->|"20% Quest Drop"| D2["⚔️ Nottingham Iron (Soulbound)"]
    B -->|"Calibrated Drops"| D3["Baskets (0.5%), Elixirs (0.8%), Mead (0.00125%), Bow (0.0000125%)"]
    
    C & D1 & D2 -->|"Camp Blacksmith"| E["Forge Finished Weapons & Gear<br>(750 Gilded Bows / 250 Drop Slots)"]
    C -->|"Pantry Sink: 14 Gold"| F["Feast Basket Rations<br>(+7 Days Sustenance; Max 56d)"]
    C -->|"Rescue Post: 20-40 Gold"| G["Mother Meg Pet Adoption<br>(Hound, Falcon, Owl)"]
    
    E & F & G -->|"100% Gold Burned"| K["OpenZeppelin _burn()<br>25% to Rebate Reserve • 75% Permanent Deflation"]
```

### 1. Macro-Economic Bounds:
At full capacity of 10,000 Hoods:
- **Expected Baseline Gross Output:** **`100,000 Gold/day`** (10,000 Hoods × 5 base heists × 2.0 avg gold).
- **Expected Fully-Buffed + Elixir Output:** **`280,000 Gold/day`** (10,000 Hoods × 10 heists × 2.0 avg gold × 1.40 max bonus).
- **Mathematical Gross Absolute Ceiling:** **`420,000 Gold/day`** (10,000 Hoods × 10 heists × 3.0 max roll × 1.40 max bonus).

### 2. Complete Batch Heist & Mixed Stamina State Machine:
Robinhood Chain executes on Arbitrum Nitro. Randomness is resolved via the `ArbSys` precompile at `0x0000000000000000000000000000000000000064`.

To strictly eliminate the **Loadout Modification Exploit**, all combat attributes, hunger states, companion bonuses, and initial fatigue flags are captured in a `HeistSnapshot` at request time. Resolution uses **ONLY the snapshot**, completely ignoring post-request equipment changes.

```solidity
struct HeistSnapshot {
    uint8 atk;
    uint8 def;
    uint8 stealth;
    uint16 critBps;
    uint16 goldBonusBps;
    uint16 economicRewardBps;
    bool initialFatigue;
}

struct HeistRequest {
    uint256 hoodId;
    uint256 targetBlock;
    uint8 count;          // 1 to 5
    uint8 baseCount;      // Rolls i < baseCount are BASE rolls
    uint8 bonusCount;     // Rolls i >= baseCount are BONUS rolls
    uint32 monthEpochAtRequest;
    bytes32 heroSeed;
    HeistSnapshot snapshot;
}

struct RewardBundle {
    uint256 gold;
    uint256 yew;
    uint256 iron;
    uint256 mead;
    uint256 baskets;
    uint256 elixirs;
    uint256 gildedBows;
    uint256 yewLongbows;
    uint256 quarterstaffs;
    uint256 poacherDaggers;
}

mapping(uint256 => RewardBundle) public unclaimedHeistRewards;
mapping(uint256 => HeistRequest) public heistRequests;

function requestHeistBatch(uint256 hoodId, uint8 count) external returns (uint256 requestId) {
    require(count >= 1 && count <= 5, "Count must be 1..5");
    require(msg.sender == hoodContract.ownerOf(hoodId) || hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
    require(!hoodContract.economicActionsPaused(), "Economic actions paused");
    require(!hoodContract.pendingNormalHeist(hoodId), "Pending heist batch already exists");
    
    bytes32 seed = hoodContract.heroSeed(hoodId);
    require(seed != bytes32(0), "Hero seed not finalized");
    
    (uint8 baseConsumed, uint8 bonusConsumed) = hoodContract.consumeStaminaBatch(hoodId, count);
    
    HeistSnapshot memory snap = hoodContract.captureHeistSnapshot(hoodId);
    
    requestId = ++nonce;
    uint256 target = ArbSys(address(0x64)).arbBlockNumber() + 2;
    
    heistRequests[requestId] = HeistRequest({
        hoodId: hoodId,
        targetBlock: target,
        count: count,
        baseCount: baseConsumed,
        bonusCount: bonusConsumed,
        monthEpochAtRequest: currentMonthEpoch(),
        heroSeed: seed,
        snapshot: snap
    });
    
    hoodContract.setPendingNormalHeist(hoodId, true);
    hoodContract.incrementPendingGameplay(hoodId, count);
    pendingRequestsByEngine[address(this)]++;
    emit HeistBatchRequested(requestId, hoodId, count, target);
}

function resolveHeist(uint256 requestId) external nonReentrant {
    HeistRequest memory req = heistRequests[requestId];
    require(req.targetBlock > 0, "Non-existent request");
    
    uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
    require(currentBlock > req.targetBlock, "Target block not reached");
    
    delete heistRequests[requestId];
    hoodContract.setPendingNormalHeist(req.hoodId, false);
    hoodContract.decrementPendingGameplay(req.hoodId, req.count);
    
    RewardBundle memory bundle;
    bool fatigueActive = req.snapshot.initialFatigue;
    
    if (req.baseCount > 0) {
        _syncMonthlyActiveHood(req.hoodId, req.monthEpochAtRequest);
    }
    
    if (currentBlock <= req.targetBlock + 256) {
        bytes32 arbHash = ArbSys(address(0x64)).arbBlockHash(req.targetBlock);
        for (uint8 i = 0; i < req.count; i++) {
            bool isBonusRoll = (i >= req.baseCount);
            fatigueActive = _resolveSequentialRoll(
                req.hoodId,
                req.snapshot,
                arbHash,
                requestId,
                i,
                isBonusRoll,
                fatigueActive,
                bundle
            );
        }
        emit HeistBatchResolved(requestId, req.hoodId, req.count);
    } else {
        for (uint8 i = 0; i < req.count; i++) {
            _resolveFallbackRoll(req.hoodId, req.snapshot, bundle);
        }
        fatigueActive = false;
        emit HeistFallbackResolved(requestId, req.hoodId, req.count);
    }
    
    hoodContract.setFatigue(req.hoodId, fatigueActive);
    _accrueRewardBundle(req.hoodId, bundle);
    
    // Engine obligation decremented AFTER reservations in _accrueRewardBundle to preserve reservation authority
    pendingRequestsByEngine[address(this)]--;
}

function _resolveSequentialRoll(
    uint256 hoodId,
    HeistSnapshot memory snap,
    bytes32 arbHash,
    uint256 requestId,
    uint8 rollIndex,
    bool isBonusRoll,
    bool currentFatigue,
    RewardBundle memory bundle
) internal returns (bool nextFatigue) {
    // 1. Difficulty & Combat Power Equation (HQ-COMBAT-001)
    bytes32 combatEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMBAT"));
    uint256 difficulty = 50 + (uint256(combatEntropy) % 51); // 50..100
    
    bytes32 critEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "CRIT"));
    bool isCrit = (uint256(critEntropy) % 10000) < snap.critBps;
    
    uint256 power = 50 + snap.atk + (snap.stealth / 2) + (isCrit ? 15 : 0);
    
    // 2. Fatigue Generation & Next-Roll Propagation (HQ-COMBAT-002)
    if (power < difficulty) {
        uint256 delta = difficulty - power;
        uint256 mitigatedDamage = (delta * (3000 - uint256(snap.def) * 100)) / 3000;
        nextFatigue = (mitigatedDamage > 20);
    } else {
        nextFatigue = false;
    }
    
    // 3. Rare Drop Multiplier (Clamped between 1.0x and 2.0x)
    int256 deltaPower = int256(power) - int256(difficulty);
    int256 rareCalc = 10000 + deltaPower * 100;
    uint256 combatBps;
    if (rareCalc < 10000) combatBps = 10000;
    else if (rareCalc > 20000) combatBps = 20000;
    else combatBps = uint256(rareCalc);
    
    // 4. Fixed-Point Gold Pipeline & Starvation / Gold-Bonus Carry (HQ-ECO-001)
    bytes32 goldEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GOLD"));
    uint256 baseGold = 1 + (uint256(goldEntropy) % 3); // 1, 2, or 3 Gold
    uint256 scaledGold = Math.mulDiv(
        baseGold,
        (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps),
        10_000 * 10_000
    );
    bundle.gold += scaledGold;
    
    // 5. Probabilistic Drops: Yew, Iron, Consumables, Gear
    bytes32 yewEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "YEW"));
    if ((uint256(yewEntropy) % DROP_SCALE) < effectiveChance(CHANCE_SHERWOOD_YEW, combatBps, currentFatigue, snap.economicRewardBps)) {
        bundle.yew += 1;
    }
    
    bytes32 ironEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "IRON"));
    if ((uint256(ironEntropy) % DROP_SCALE) < effectiveChance(CHANCE_NOTTINGHAM_IRON, combatBps, currentFatigue, snap.economicRewardBps)) {
        bundle.iron += 1;
    }
    
    bytes32 basketEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "BASKET"));
    if ((uint256(basketEntropy) % DROP_SCALE) < effectiveChance(CHANCE_FEAST_BASKET, combatBps, currentFatigue, snap.economicRewardBps)) {
        bundle.baskets += 1;
    }
    
    // Greenwood Elixir (0.8% - strictly BASE rolls only)
    if (!isBonusRoll) {
        bytes32 elixirEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "ELIXIR"));
        if ((uint256(elixirEntropy) % DROP_SCALE) < effectiveChance(CHANCE_GREENWOOD_ELIXIR, combatBps, currentFatigue, snap.economicRewardBps)) {
            bundle.elixirs += 1;
        }
    }
    
    bytes32 meadEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "MEAD"));
    if ((uint256(meadEntropy) % DROP_SCALE) < effectiveChance(CHANCE_MEAD_CASK, combatBps, currentFatigue, snap.economicRewardBps)) {
        bundle.mead += 1;
    }
    
    bytes32 gildedEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GILDED"));
    if ((uint256(gildedEntropy) % DROP_SCALE) < effectiveChance(CHANCE_GILDED_BOW, combatBps, currentFatigue, snap.economicRewardBps)) {
        bundle.gildedBows += 1;
    }
    
    // Common Finished Weapons (0.00025%) with 3-way split
    bytes32 commonEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMMON_WEAPON"));
    if ((uint256(commonEntropy) % DROP_SCALE) < effectiveChance(CHANCE_COMMON_WEAPON, combatBps, currentFatigue, snap.economicRewardBps)) {
        bytes32 typeEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMMON_WEAPON_TYPE"));
        uint256 wType = uint256(typeEntropy) % 3;
        if (wType == 0) bundle.yewLongbows += 1;
        else if (wType == 1) bundle.quarterstaffs += 1;
        else bundle.poacherDaggers += 1;
    }
}

function _resolveFallbackRoll(
    uint256 hoodId,
    HeistSnapshot memory snap,
    RewardBundle memory bundle
) internal pure {
    uint256 gold = Math.mulDiv(
        1,
        (10000 + uint256(snap.goldBonusBps)) * uint256(snap.economicRewardBps),
        10_000 * 10_000
    );
    bundle.gold += gold > 0 ? gold : 1; // Minimum 1 gold on fallback
}

function _accrueRewardBundle(uint256 hoodId, RewardBundle memory bundle) internal {
    RewardBundle storage existing = unclaimedHeistRewards[hoodId];
    bool previouslyZero = (
        existing.gold == 0 && existing.yew == 0 && existing.iron == 0 &&
        existing.baskets == 0 && existing.elixirs == 0 && existing.mead == 0 &&
        existing.gildedBows == 0 && existing.yewLongbows == 0 &&
        existing.quarterstaffs == 0 && existing.poacherDaggers == 0
    );
    
    // Convert scarce drops into Treasury reservations with multi-unit support
    if (bundle.gildedBows > 0) {
        uint256 granted = treasuresContract.reserveItem(GILDED_BOW, MintSource.DROP, bundle.gildedBows);
        if (granted < bundle.gildedBows) {
            emit CappedDropSkipped(hoodId, GILDED_BOW, bundle.gildedBows - granted);
            bundle.gildedBows = granted;
        }
    }
    if (bundle.elixirs > 0) {
        uint256 granted = treasuresContract.reserveItem(ELIXIR, MintSource.DROP, bundle.elixirs);
        if (granted < bundle.elixirs) {
            emit CappedDropSkipped(hoodId, ELIXIR, bundle.elixirs - granted);
            bundle.elixirs = granted;
        }
    }
    if (bundle.mead > 0) {
        uint256 granted = treasuresContract.reserveItem(MEAD, MintSource.DROP, bundle.mead);
        if (granted < bundle.mead) {
            emit CappedDropSkipped(hoodId, MEAD, bundle.mead - granted);
            bundle.mead = granted;
        }
    }
    if (bundle.yewLongbows > 0) {
        uint256 granted = treasuresContract.reserveItem(YEW_LONGBOW, MintSource.DROP, bundle.yewLongbows);
        if (granted < bundle.yewLongbows) {
            emit CappedDropSkipped(hoodId, YEW_LONGBOW, bundle.yewLongbows - granted);
            bundle.yewLongbows = granted;
        }
    }
    if (bundle.quarterstaffs > 0) {
        uint256 granted = treasuresContract.reserveItem(QUARTERSTAFF, MintSource.DROP, bundle.quarterstaffs);
        if (granted < bundle.quarterstaffs) {
            emit CappedDropSkipped(hoodId, QUARTERSTAFF, bundle.quarterstaffs - granted);
            bundle.quarterstaffs = granted;
        }
    }
    if (bundle.poacherDaggers > 0) {
        uint256 granted = treasuresContract.reserveItem(POACHER_DAGGERS, MintSource.DROP, bundle.poacherDaggers);
        if (granted < bundle.poacherDaggers) {
            emit CappedDropSkipped(hoodId, POACHER_DAGGERS, bundle.poacherDaggers - granted);
            bundle.poacherDaggers = granted;
        }
    }
    
    // Merge into Hood entitlement
    existing.gold += bundle.gold;
    existing.yew += bundle.yew;
    existing.iron += bundle.iron;
    existing.baskets += bundle.baskets;
    existing.elixirs += bundle.elixirs;
    existing.mead += bundle.mead;
    existing.gildedBows += bundle.gildedBows;
    existing.yewLongbows += bundle.yewLongbows;
    existing.quarterstaffs += bundle.quarterstaffs;
    existing.poacherDaggers += bundle.poacherDaggers;
    
    // Compute final non-zero state strictly AFTER reservations/skips to prevent orphaned counters
    bool finalBundleNonZero = (
        bundle.gold > 0 || bundle.yew > 0 || bundle.iron > 0 ||
        bundle.baskets > 0 || bundle.elixirs > 0 || bundle.mead > 0 ||
        bundle.gildedBows > 0 || bundle.yewLongbows > 0 ||
        bundle.quarterstaffs > 0 || bundle.poacherDaggers > 0
    );
    
    if (previouslyZero && finalBundleNonZero) {
        outstandingRewardClaimsByEngine[address(this)]++;
        hoodContract.incrementPendingHeistReward(hoodId);
    }
}

function claimHeistRewards(uint256 hoodId, address recipient) external nonReentrant {
    address owner = hoodContract.ownerOf(hoodId);
    if (msg.sender != owner) {
        require(hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(recipient == owner, "Delegates can only claim to Hood owner");
    }
    require(recipient != address(0), "Invalid recipient");
    
    RewardBundle memory bundle = unclaimedHeistRewards[hoodId];
    require(
        bundle.gold > 0 || bundle.yew > 0 || bundle.iron > 0 ||
        bundle.baskets > 0 || bundle.elixirs > 0 || bundle.mead > 0 ||
        bundle.gildedBows > 0 || bundle.yewLongbows > 0 ||
        bundle.quarterstaffs > 0 || bundle.poacherDaggers > 0,
        "No rewards to claim"
    );
    
    delete unclaimedHeistRewards[hoodId];
    outstandingRewardClaimsByEngine[address(this)]--;
    hoodContract.decrementPendingHeistReward(hoodId);
    treasuresContract.settleHeistRewardBundle(recipient, bundle);
    emit HeistRewardsClaimed(hoodId, recipient);
}
```

### 3. Precision Drop Rates & 10 Domain-Separated Sub-Rolls:
Probabilities are scaled by `DROP_SCALE = 1_000_000_000` ($10^9$):
```solidity
uint256 constant DROP_SCALE = 1_000_000_000;

uint256 constant CHANCE_GILDED_BOW      =         125; // 0.0000125%
uint256 constant CHANCE_COMMON_WEAPON   =       2_500; // 0.00025%
uint256 constant CHANCE_MEAD_CASK       =      12_500; // 0.00125%
uint256 constant CHANCE_FEAST_BASKET    =   5_000_000; // 0.5%
uint256 constant CHANCE_GREENWOOD_ELIXIR=   8_000_000; // 0.8%
uint256 constant CHANCE_SHERWOOD_YEW    = 250_000_000; // 25.0%
uint256 constant CHANCE_NOTTINGHAM_IRON = 200_000_000; // 20.0%
```

Every sub-roll uses a dedicated domain string to guarantee complete statistical independence:
```solidity
bytes32 goldEntropy   = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GOLD"));
bytes32 critEntropy   = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "CRIT"));
bytes32 yewEntropy    = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "YEW"));
bytes32 ironEntropy   = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "IRON"));
bytes32 gildedEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "GILDED"));
bytes32 commonEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMMON_WEAPON"));
bytes32 typeEntropy   = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "COMMON_WEAPON_TYPE"));
bytes32 meadEntropy   = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "MEAD"));
bytes32 basketEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "BASKET"));
bytes32 elixirEntropy = keccak256(abi.encode(arbHash, requestId, hoodId, rollIndex, "ELIXIR"));
```

Universal Multiplier:
```solidity
function effectiveChance(
    uint256 baseChance,
    uint256 combatBps,
    bool isFatigued,
    uint256 economicRewardBps
) internal pure returns (uint256) {
    uint256 fatigueBps = isFatigued ? 7500 : 10_000;
    return Math.mulDiv(
        baseChance,
        combatBps * fatigueBps * economicRewardBps,
        10_000 * 10_000 * 10_000
    );
}
```
*`effectiveChance()` applies to probabilistic economic drops: materials (Yew & Iron), consumables, and gear. Gold quantity uses the fixed-point starvation + Gold-bonus pipeline and is NOT multiplied by combat drop chance.*

### 4. Stamina & Elixir Execution State Machine:
```solidity
function consumeStaminaBatch(uint256 hoodId, uint8 count) external onlyRaidEngine returns (uint8 baseConsumed, uint8 bonusConsumed) {
    if (currentUtcDay() > lastHeistDay[hoodId]) {
        baseHeistsUsed[hoodId] = 0;
        bonusHeistsUsed[hoodId] = 0;
        lastHeistDay[hoodId] = currentUtcDay();
    }
    
    uint8 baseRemaining = 5 - baseHeistsUsed[hoodId];
    if (count <= baseRemaining) {
        baseHeistsUsed[hoodId] += count;
        return (count, 0);
    } else {
        baseConsumed = baseRemaining;
        bonusConsumed = count - baseConsumed;
        require(lastElixirDay[hoodId] == currentUtcDay(), "Bonus stamina not unlocked");
        require(bonusHeistsUsed[hoodId] + bonusConsumed <= 5, "Exceeds daily bonus stamina");
        baseHeistsUsed[hoodId] = 5;
        bonusHeistsUsed[hoodId] += bonusConsumed;
        return (baseConsumed, bonusConsumed);
    }
}

function useElixir(uint256 hoodId) external {
    require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(!economicActionsPaused(), "Economic actions paused");
    require(!isSlumbering(hoodId), "Hero is slumbering");
    require(lastElixirDay[hoodId] < currentUtcDay(), "Elixir already used today");
    
    // Burns Elixir strictly from caller's wallet
    treasuresContract.burnElixir(msg.sender, 1);
    lastElixirDay[hoodId] = currentUtcDay();
    emit ElixirUsed(hoodId, currentUtcDay());
}
```

---
"""

def build_section_4():
    return r"""## 4. The Armory Escrow Vault & Bazaar Custody Engine

### 1. Canonical Slots & Aggregate Custody:
`0: Weapon`, `1: Armor`, `2: Ammo`, `3: Utility`, `4: SustenanceRelic`, `5: Decor`, `6: Companion`.
- Reverse binding for ERC-1155 gear uses aggregate vault custody: `boundCount[itemId]`.
- Vault Invariant: `Treasury.balanceOf(HoodQuestVault, itemId) == boundCount[itemId]`.
- Companions (ERC-721) maintain authoritative reverse mapping in HoodQuest core: `petBoundToHood[petId] == hoodId`.

### 2. Executable Armory State Machine:
```solidity
struct UnequipRequest {
    uint64 maturesAt;
    uint32 itemId;
}

mapping(uint32 => uint8) public canonicalItemSlot;
mapping(uint32 => bool) public isEquippable;
mapping(uint256 => mapping(uint8 => uint32)) public equippedSlot; // hoodId => slot => itemId
mapping(uint256 => mapping(uint8 => UnequipRequest)) public pendingUnequip;
mapping(uint256 => uint8) public pendingUnequipCount;
mapping(uint256 => uint64) public postTransferUnequipLockedUntil;
mapping(uint256 => uint64) public cornucopiaBoundTimestamp;

function equipItem(uint256 hoodId, uint8 slot, uint32 itemId) external nonReentrant {
    require(msg.sender == ownerOf(hoodId), "Not owner");
    require(slot <= 5, "Invalid gear slot");
    require(isEquippable[itemId], "Item not equippable");
    require(canonicalItemSlot[itemId] == slot, "Item does not belong in this slot");
    require(equippedSlot[hoodId][slot] == 0, "Slot occupied: unequip first");
    require(pendingUnequip[hoodId][slot].maturesAt == 0, "Unequip notice active");
    require(block.timestamp >= postTransferUnequipLockedUntil[hoodId], "Post-transfer unequip lock active");
    
    if (slot == 2 && itemId == GOLDEN_ARROW) {
        uint32 w = equippedSlot[hoodId][0];
        require(w == GILDED_BOW || w == YEW_LONGBOW, "Golden Arrow requires bow");
    }
    
    equippedSlot[hoodId][slot] = itemId;
    boundCount[itemId]++;
    if (slot == 4 && itemId == FRIARS_CORNUCOPIA) {
        cornucopiaBoundTimestamp[hoodId] = uint64(block.timestamp);
    }
    
    treasuresContract.safeTransferFrom(msg.sender, address(this), itemId, 1, "");
    loadoutVersion[hoodId]++;
    emit MetadataUpdate(hoodId);
    emit ItemEquipped(hoodId, slot, itemId);
}

function initiateUnequip(uint256 hoodId, uint8 slot) external {
    require(msg.sender == ownerOf(hoodId), "Not owner");
    uint32 itemId = equippedSlot[hoodId][slot];
    require(itemId != 0, "Slot is empty");
    require(pendingUnequip[hoodId][slot].maturesAt == 0, "Already initiated");
    require(block.timestamp >= postTransferUnequipLockedUntil[hoodId], "Post-transfer lock active");
    
    if (slot == 0) {
        require(equippedSlot[hoodId][2] != GOLDEN_ARROW, "Unequip ammo first");
    }
    if (slot == 4 && itemId == FRIARS_CORNUCOPIA) {
        require(block.timestamp >= cornucopiaBoundTimestamp[hoodId] + 7 days, "Cornucopia 7-day bind lock active");
    }
    
    pendingUnequip[hoodId][slot] = UnequipRequest(uint64(block.timestamp + 24 hours), itemId);
    pendingUnequipCount[hoodId]++;
    emit UnequipInitiated(hoodId, slot, itemId, block.timestamp + 24 hours);
}

function finalizeUnequip(uint256 hoodId, uint8 slot) external nonReentrant {
    require(msg.sender == ownerOf(hoodId), "Not owner");
    UnequipRequest memory req = pendingUnequip[hoodId][slot];
    require(req.maturesAt > 0, "No pending unequip");
    require(block.timestamp >= req.maturesAt, "Maturation period not reached");
    require(equippedSlot[hoodId][slot] == req.itemId, "Item mismatch");
    
    delete pendingUnequip[hoodId][slot];
    pendingUnequipCount[hoodId]--;
    equippedSlot[hoodId][slot] = 0;
    boundCount[req.itemId]--;
    
    loadoutVersion[hoodId]++;
    emit MetadataUpdate(hoodId);
    treasuresContract.safeTransferFrom(address(this), msg.sender, req.itemId, 1, "");
    emit UnequipFinalized(hoodId, slot, req.itemId);
}
```

### 3. Executable Companion Bonding State Machine:
```solidity
mapping(uint256 => uint256) public petBoundToHood; // petId => hoodId
mapping(uint256 => uint256) public hoodBoundPet;   // hoodId => petId
mapping(uint256 => uint64) public petBondedAt;
mapping(uint256 => uint64) public pendingDebondMaturesAt;

function bondPet(uint256 hoodId, uint256 petId) external nonReentrant {
    require(msg.sender == ownerOf(hoodId), "Not Hood owner");
    require(companionContract.ownerOf(petId) == msg.sender, "Not pet owner");
    require(hoodBoundPet[hoodId] == 0, "Hood already has companion");
    require(petBoundToHood[petId] == 0, "Pet already bonded");
    
    petBoundToHood[petId] = hoodId;
    hoodBoundPet[hoodId] = petId;
    petBondedAt[petId] = uint64(block.timestamp);
    companionContract.recordBondAge(petId, effectiveBiologicalAge(hoodId));
    
    expectedPetDeposit[petId] = msg.sender;
    companionContract.safeTransferFrom(msg.sender, address(this), petId);
    delete expectedPetDeposit[petId];
    
    loadoutVersion[hoodId]++;
    emit MetadataUpdate(hoodId);
    emit PetBonded(hoodId, petId);
}

function initiateDebond(uint256 hoodId) external {
    require(msg.sender == ownerOf(hoodId), "Not Hood owner");
    uint256 petId = hoodBoundPet[hoodId];
    require(petId != 0, "No pet bonded");
    require(block.timestamp >= petBondedAt[petId] + 12 hours, "12h initial bond lock active");
    require(pendingDebondMaturesAt[hoodId] == 0, "Debond already active");
    
    pendingDebondMaturesAt[hoodId] = uint64(block.timestamp + 12 hours);
    emit DebondInitiated(hoodId, petId, block.timestamp + 12 hours);
}

function finalizeDebond(uint256 hoodId) external nonReentrant {
    require(msg.sender == ownerOf(hoodId), "Not Hood owner");
    require(pendingDebondMaturesAt[hoodId] > 0, "No pending debond");
    require(block.timestamp >= pendingDebondMaturesAt[hoodId], "Debond timer not mature");
    
    uint256 petId = hoodBoundPet[hoodId];
    delete pendingDebondMaturesAt[hoodId];
    delete hoodBoundPet[hoodId];
    delete petBoundToHood[petId];
    
    companionContract.settleDebondAge(petId, effectiveBiologicalAge(hoodId));
    
    loadoutVersion[hoodId]++;
    emit MetadataUpdate(hoodId);
    companionContract.safeTransferFrom(address(this), msg.sender, petId);
    emit DebondFinalized(hoodId, petId);
}
```

### 4. Typed `getLoadoutHash(hoodId)`:
```solidity
function getLoadoutHash(uint256 hoodId) public view returns (bytes32) {
    return keccak256(abi.encode(
        equippedSlot[hoodId][0], // weapon
        equippedSlot[hoodId][1], // armor
        equippedSlot[hoodId][2], // ammo
        equippedSlot[hoodId][3], // utility
        equippedSlot[hoodId][4], // sustenanceRelic
        equippedSlot[hoodId][5], // decor
        hoodBoundPet[hoodId],    // companion
        loadoutVersion[hoodId]
    ));
}
```

### 5. Executable Native Camp Bazaar State Machine:
```solidity
struct Listing {
    address seller;
    uint256 price;
    bytes32 loadoutHash;
}

mapping(uint256 => Listing) public listings;
mapping(address => uint256) public bazaarProceedsEscrow;
uint256[] public activeListingTokenIds;
mapping(uint256 => uint256) public activeListingIndexPlusOne; // 0 = not listed
mapping(uint256 => address) public expectedDeposit;

function listHero(uint256 hoodId, uint256 price) external nonReentrant {
    require(price > 0, "Price must be > 0");
    require(hoodContract.ownerOf(hoodId) == msg.sender, "Not owner");
    (bool allowed, uint256 reasonFlags) = hoodContract.canList(hoodId);
    require(allowed, "Pre-sale check failed");
    
    bytes32 lHash = hoodContract.getLoadoutHash(hoodId);
    listings[hoodId] = Listing({
        seller: msg.sender,
        price: price,
        loadoutHash: lHash
    });
    
    activeListingTokenIds.push(hoodId);
    activeListingIndexPlusOne[hoodId] = activeListingTokenIds.length;
    
    expectedDeposit[hoodId] = msg.sender;
    hoodContract.safeTransferFrom(msg.sender, address(this), hoodId);
    delete expectedDeposit[hoodId];
    
    emit HeroListed(hoodId, msg.sender, price, lHash);
}

function cancelListing(uint256 hoodId) external nonReentrant {
    Listing memory l = listings[hoodId];
    require(l.seller == msg.sender, "Not seller");
    
    delete listings[hoodId];
    _removeActiveListing(hoodId);
    
    hoodContract.setBazaarTransferMode(HoodQuest.BazaarTransferMode.CANCEL_WITHDRAWAL);
    hoodContract.safeTransferFrom(address(this), msg.sender, hoodId);
    hoodContract.setBazaarTransferMode(HoodQuest.BazaarTransferMode.NONE);
    
    emit ListingCancelled(hoodId, msg.sender);
}

function buyListing(uint256 hoodId) external nonReentrant {
    Listing memory l = listings[hoodId];
    require(l.price > 0, "Not listed");
    require(msg.sender != l.seller, "Cannot buy own listing");
    
    bytes32 currentHash = hoodContract.getLoadoutHash(hoodId);
    require(currentHash == l.loadoutHash, "Loadout modified while listed");
    
    delete listings[hoodId];
    _removeActiveListing(hoodId);
    
    uint256 fee = (l.price * 250) / 10_000; // 2.5% protocol fee
    uint256 sellerProceeds = treasuresContract.settleBazaarPayment(msg.sender, l.seller, l.price, fee);
    bazaarProceedsEscrow[l.seller] += sellerProceeds;
    
    hoodContract.setBazaarTransferMode(HoodQuest.BazaarTransferMode.SALE_PURCHASE);
    hoodContract.safeTransferFrom(address(this), msg.sender, hoodId);
    hoodContract.setBazaarTransferMode(HoodQuest.BazaarTransferMode.NONE);
    
    emit HeroSold(hoodId, l.seller, msg.sender, l.price, fee);
}

function withdrawBazaarProceeds() external nonReentrant {
    uint256 amount = bazaarProceedsEscrow[msg.sender];
    require(amount > 0, "No proceeds");
    
    bazaarProceedsEscrow[msg.sender] = 0;
    treasuresContract.safeTransferFrom(address(this), msg.sender, 1, amount, "");
    emit ProceedsWithdrawn(msg.sender, amount);
}

function _removeActiveListing(uint256 hoodId) internal {
    uint256 indexPlusOne = activeListingIndexPlusOne[hoodId];
    require(indexPlusOne > 0, "Not in active listings");
    uint256 index = indexPlusOne - 1;
    uint256 lastIndex = activeListingTokenIds.length - 1;
    
    if (index != lastIndex) {
        uint256 lastTokenId = activeListingTokenIds[lastIndex];
        activeListingTokenIds[index] = lastTokenId;
        activeListingIndexPlusOne[lastTokenId] = index + 1;
    }
    
    activeListingTokenIds.pop();
    delete activeListingIndexPlusOne[hoodId];
}

function getActiveListings(uint256 offset, uint256 limit) external view returns (uint256[] memory tokenIds, Listing[] memory details) {
    require(limit > 0 && limit <= 100, "Limit 1..100");
    uint256 total = activeListingTokenIds.length;
    if (offset >= total) return (new uint256[](0), new Listing[](0));
    
    uint256 end = offset + limit;
    if (end > total) end = total;
    uint256 count = end - offset;
    
    tokenIds = new uint256[](count);
    details = new Listing[](count);
    for (uint256 i = 0; i < count; i++) {
        uint256 id = activeListingTokenIds[offset + i];
        tokenIds[i] = id;
        details[i] = listings[id];
    }
}
```

---
"""

def build_section_5():
    return r"""## 5. Anti-Power-Creep Weapon Matrix & The Blacksmith

### Statutory Stat Invariants:
1. `MAX_EFFECTIVE_ATK = 45` (Gilded Bow +20 + Golden Arrow +25 apex).
2. `MAX_EFFECTIVE_DEF = 30` (Locksley Cloak +20 + Camp Hound Rank 5 +10).
3. `MAX_EFFECTIVE_STEALTH = 30` (Twin Daggers +15 + Locksley Cloak +10 + Barn Owl Rank 5 +5).
4. `MAX_EFFECTIVE_MORALE = 10` (Silver Rallying Horn +10 statutory cap).
5. `BASE_COMBAT_POWER = 50` (Baseline for ungeared Hoods).
6. `MAX_GOLD_MULTIPLIER = 40%` (Gilded Bow +20% + Owl Rank 5 +10% + Devotion +10%).
7. `MAX_CRIT_CHANCE = 8%` (Hunting Falcon Rank 5 apex).

### Complete Canonical Arsenal & Blacksmith Recipes:

| Item ID | Item Name | Canonical Slot | Supply Mode | Total Cap | Stats / Perks | Crafting Cost |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **#1** | **Royal Gold Sovereign** | Currency | Uncapped | Deflationary | Protocol Gas & Trading Currency | N/A (Heist Drops / Faucet) |
| **#2** | **Locksley Cloak** | 1 (Armor) | Circulating | 2,500 | +20 DEF, +10 Stealth | 100 Gold + 10 Yew |
| **#3** | **Gilded Recurve Bow** | 0 (Weapon) | **Split (750/250)** | **1,000 Total** | +20 ATK, +20% Gold Drop | 250 Gold + 25 Yew + 10 Iron |
| **#4** | **The Golden Arrow** | 2 (Ammo) | **Lifetime Grail** | **25 Total** | +25 ATK (Requires Bow) | Uncraftable (Championship Only) |
| **#5** | **Yew Longbow** | 0 (Weapon) | Circulating | 5,000 | +12 ATK | 40 Gold + 8 Yew |
| **#6** | **Hardened Quarterstaff** | 0 (Weapon) | Circulating | 5,000 | +8 ATK, +6 DEF | 35 Gold + 6 Yew + 2 Iron |
| **#7** | **Poacher's Twin Daggers**| 0 (Weapon) | Circulating | 5,000 | +10 ATK, +15 Stealth | 40 Gold + 4 Yew + 6 Iron |
| **#8** | **Silver Rallying Horn** | 3 (Utility) | Circulating | 2,500 | +10 Morale | 75 Gold + 12 Iron |
| **#9** | **Friar's Cornucopia** | 4 (Sustenance) | **Lifetime Grail** | **25 Total** | Zero Upkeep Cost (Immortal Sustenance) | Uncraftable (5-Year Jubilee Only) |
| **#13** | **Feast Basket** | Consumable | Uncapped | Consumable | +7 Days Rations Sustenance | 14 Gold (Pantry Store) |
| **#14** | **Greenwood Elixir** | Consumable | Circulating | 5,000 | +5 Bonus Heists/Day | Uncraftable (Quest Drop Only) |
| **#15** | **Mead Cask** | Consumable | Circulating | 1,000 | Instantly Clears Fatigue | Uncraftable (0.00125% Drop) |
| **#16** | **Sherwood Yew** | Material | Uncapped | **Soulbound** | Primary Weapon/Bow Crafting | Quest Drop (25%) / Falcon Forage |
| **#17** | **Nottingham Iron** | Material | Uncapped | **Soulbound** | Primary Armor/Dagger Crafting | Quest Drop (20%) / Hound Forage |

*IDs 10–12 and 18–20 are permanently `RESERVED_UNMINTABLE` in V1.*

### The Blacksmith Crafting Execution State Machine:
```solidity
function craft(uint256 itemId, uint256 quantity) external nonReentrant {
    require(quantity > 0, "Quantity must be > 0");
    require(!hoodContract.economicActionsPaused(), "Economic actions paused");
    
    CraftRecipe memory r = craftRecipes[itemId];
    require(r.isValid, "Item not craftable");
    
    if (r.mode == SupplyMode.SPLIT && itemId == GILDED_BOW) {
        require(forgedGildedBows + quantity <= 750, "Forge cap reached");
        forgedGildedBows += quantity;
    } else if (r.mode == SupplyMode.MAX_LIFETIME) {
        require(lifetimeMinted[itemId] + reservedUnclaimed[itemId] + quantity <= r.cap, "Lifetime cap reached");
    } else if (r.mode == SupplyMode.MAX_CIRCULATING) {
        require(totalSupply(itemId) + reservedUnclaimed[itemId] + quantity <= r.cap, "Circulating cap reached");
    }
    
    _burnGold(msg.sender, r.goldCost * quantity);
    if (r.yewCost > 0) _burn(msg.sender, YEW, r.yewCost * quantity);
    if (r.ironCost > 0) _burn(msg.sender, IRON, r.ironCost * quantity);
    
    lifetimeMinted[itemId] += quantity;
    _mint(msg.sender, itemId, quantity, "");
    emit ItemCrafted(msg.sender, itemId, quantity);
}
```

### Strict Caller Domain Privilege Wrappers & Heist Bundle Settlement (HQ-TREAS-008):
```solidity
function burnAdoptionGold(address from, uint256 amount) external onlyCompanions {
    _burnGold(from, amount);
}

function mintForageMaterial(address to, uint256 itemId, uint256 amount) external onlyCompanions {
    require(itemId == YEW || itemId == IRON, "Invalid forage item");
    _mint(to, itemId, amount, "");
}

function burnElixir(address from, uint256 amount) external onlyHoodQuest {
    _burn(from, ELIXIR, amount);
}

function burnRationBasket(address from, uint256 amount) external onlyHoodQuest {
    _burn(from, BASKET, amount);
}

function settleBazaarPayment(
    address buyer,
    address seller,
    uint256 price,
    uint256 fee
) external onlyBazaar nonReentrant returns (uint256 sellerProceeds) {
    require(price >= fee, "Fee exceeds price");
    sellerProceeds = price - fee;
    
    _burnGold(buyer, fee);
    _safeTransferFrom(buyer, msg.sender, 1, sellerProceeds, "");
    emit BazaarPaymentSettled(buyer, seller, price, fee);
}

function settleHeistRewardBundle(address to, RewardBundle calldata bundle) external onlySettlementApproved nonReentrant {
    if (bundle.gold > 0) _mint(to, 1, bundle.gold, "");
    if (bundle.yew > 0) _mint(to, YEW, bundle.yew, "");
    if (bundle.iron > 0) _mint(to, IRON, bundle.iron, "");
    
    if (bundle.baskets > 0) {
        lifetimeMinted[BASKET] += bundle.baskets;
        _mint(to, BASKET, bundle.baskets, "");
    }
    if (bundle.elixirs > 0) {
        reservedUnclaimed[ELIXIR] -= bundle.elixirs;
        lifetimeMinted[ELIXIR] += bundle.elixirs;
        _mint(to, ELIXIR, bundle.elixirs, "");
    }
    if (bundle.mead > 0) {
        reservedUnclaimed[MEAD] -= bundle.mead;
        lifetimeMinted[MEAD] += bundle.mead;
        _mint(to, MEAD, bundle.mead, "");
    }
    if (bundle.gildedBows > 0) {
        dropReservedGildedBows -= bundle.gildedBows;
        reservedUnclaimed[GILDED_BOW] -= bundle.gildedBows;
        droppedGildedBows += bundle.gildedBows;
        lifetimeMinted[GILDED_BOW] += bundle.gildedBows;
        _mint(to, GILDED_BOW, bundle.gildedBows, "");
    }
    if (bundle.yewLongbows > 0) {
        reservedUnclaimed[YEW_LONGBOW] -= bundle.yewLongbows;
        lifetimeMinted[YEW_LONGBOW] += bundle.yewLongbows;
        _mint(to, YEW_LONGBOW, bundle.yewLongbows, "");
    }
    if (bundle.quarterstaffs > 0) {
        reservedUnclaimed[QUARTERSTAFF] -= bundle.quarterstaffs;
        lifetimeMinted[QUARTERSTAFF] += bundle.quarterstaffs;
        _mint(to, QUARTERSTAFF, bundle.quarterstaffs, "");
    }
    if (bundle.poacherDaggers > 0) {
        reservedUnclaimed[POACHER_DAGGERS] -= bundle.poacherDaggers;
        lifetimeMinted[POACHER_DAGGERS] += bundle.poacherDaggers;
        _mint(to, POACHER_DAGGERS, bundle.poacherDaggers, "");
    }
}
```

---
"""

def build_section_6():
    return r"""## 6. Mother Meg's Rescue Post & Companion Sidecars

Companions are managed by `HoodQuestCompanions.sol`:
- **Supply Cap:** **10,000 Total Genesis Companions** (4,000 Hounds, 3,000 Falcons, 3,000 Owls).
- **Pet Biological Age Clock:**
  ```solidity
  function effectivePetAge(uint256 petId) public view returns (uint256) {
      uint256 hoodId = hoodContract.petBoundToHood(petId);
      if (hoodId == 0) return accumulatedPetActiveSeconds[petId];
      uint256 hoodCurrentAge = hoodContract.effectiveBiologicalAge(hoodId);
      return accumulatedPetActiveSeconds[petId] + (hoodCurrentAge - hoodEffectiveAgeAtBond[petId]);
  }
  ```
- **Pet Bond Rank XP Thresholds (Derived Strictly from petXp):**
  - **Rank 1:** `0 XP`
  - **Rank 2:** `300 XP` (~30 forage days)
  - **Rank 3:** `900 XP` (~90 forage days)
  - **Rank 4:** `1,800 XP` (~180 forage days)
  - **Rank 5:** `3,650 XP` (~365 forage days)

### Daily Solo Foraging State Machine:
```solidity
mapping(uint256 => uint32) public petLastForageDay;
mapping(uint256 => uint256) public pendingForageYew;
mapping(uint256 => uint256) public pendingForageIron;

function soloForage(uint256 petId) external returns (uint8 xpGain, uint8 mats) {
    require(msg.sender == ownerOf(petId) || isGameDelegate(petId, msg.sender), "Not authorized");
    require(currentUtcDay() > petLastForageDay[petId], "Already foraged today");
    
    uint256 hoodId = hoodContract.petBoundToHood(petId);
    require(hoodId != 0, "Must be bonded to forage");
    require(!hoodContract.isSlumbering(hoodId), "Hood is slumbering");
    
    petLastForageDay[petId] = currentUtcDay();
    petXp[petId] += 10;
    xpGain = 10;
    
    uint8 rank = bondRank(petId);
    mats = rank >= 4 ? 2 : 1;
    uint8 sp = species[petId];
    
    if (sp == 0) { // Camp Hound
        pendingForageIron[hoodId] += mats;
    } else if (sp == 1) { // Hunting Falcon
        pendingForageYew[hoodId] += mats;
    }
    emit PetForaged(petId, hoodId, mats, xpGain);
}

function claimForage(uint256 hoodId, address recipient) external nonReentrant {
    require(msg.sender == hoodContract.ownerOf(hoodId), "Not Hood owner");
    require(recipient != address(0), "Invalid recipient");
    
    uint256 yew = pendingForageYew[hoodId];
    uint256 iron = pendingForageIron[hoodId];
    require(yew > 0 || iron > 0, "No materials to claim");
    
    pendingForageYew[hoodId] = 0;
    pendingForageIron[hoodId] = 0;
    
    if (yew > 0) treasuresContract.mintForageMaterial(recipient, YEW, yew);
    if (iron > 0) treasuresContract.mintForageMaterial(recipient, IRON, iron);
    emit ForageClaimed(hoodId, recipient, yew, iron);
}
```

---
"""

def build_section_7():
    return r"""## 7. The Upkeep, Slumber & Calibrated Devotion System

### 1. Daily Care Function & Idempotent Slumber Settlement:
```solidity
function dailyCare(uint256 tokenId) external {
    require(_isApprovedOrOwner(msg.sender, tokenId) || isGameDelegate(tokenId, msg.sender), "Not authorized");
    require(lastCareDay[tokenId] < currentUtcDay(), "Already cared for today");
    
    if (slumbering[tokenId]) {
        _settleSlumber(tokenId);
        slumbering[tokenId] = false;
        emit SlumberStateChanged(tokenId, false);
    }
    
    lastCareDay[tokenId] = currentUtcDay();
    lastCareTimestamp[tokenId] = uint64(block.timestamp);
    emit DailyCareGiven(tokenId, currentUtcDay());
}

function _settleSlumber(uint256 tokenId) internal {
    uint64 current = uint64(block.timestamp);
    uint64 accounted = slumberAccountedUntil[tokenId];
    if (current > accounted) {
        totalSlumberSeconds[tokenId] += (current - accounted);
        slumberAccountedUntil[tokenId] = current;
    }
}
```

### 2. Real-Time Effective Biological Age Formula:
```solidity
function effectiveBiologicalAge(uint256 tokenId) public view returns (uint256) {
    uint256 totalElapsed = block.timestamp - mintTimestamp[tokenId];
    uint256 slumberTime = totalSlumberSeconds[tokenId];
    if (slumbering[tokenId]) {
        slumberTime += (block.timestamp - slumberAccountedUntil[tokenId]);
    }
    return totalElapsed > slumberTime ? totalElapsed - slumberTime : 0;
}
```

### 3. Starvation & 56-Day Feeding State Machine:
```solidity
function feed(uint256 tokenId) external {
    require(_isApprovedOrOwner(msg.sender, tokenId) || isGameDelegate(tokenId, msg.sender), "Not authorized");
    require(!isSlumbering(tokenId), "Hero is slumbering");
    
    uint64 currentRations = rationsUntil[tokenId];
    uint64 baseline = currentRations > block.timestamp ? currentRations : uint64(block.timestamp);
    uint64 newRations = baseline + 7 days;
    require(newRations <= block.timestamp + 56 days, "Rations exceed 56-day maximum");
    
    treasuresContract.burnRationBasket(msg.sender, 1);
    rationsUntil[tokenId] = newRations;
    emit HeroFed(tokenId, newRations);
}
```

### 4. Devotion Progression Ladder (Derived from Effective Age):
```solidity
function devotionBonusBps(uint256 tokenId) public view returns (uint16) {
    uint256 awakeDays = effectiveBiologicalAge(tokenId) / 1 days;
    if (awakeDays >= 360) return 1000; // +10% Gold (Statutory Cap)
    if (awakeDays >= 180) return 600;  // +6%
    if (awakeDays >= 90)  return 400;  // +4%
    if (awakeDays >= 30)  return 200;  // +2%
    return 0;
}
```

---
"""

def build_section_8():
    return r"""## 8. Gas-Free On-Chain Minigames & Artisan Vector Art Pipeline

### 1. Paper-Doll Generative Traits & Hand Anchoring:
- **`5 Archetypes`:** Robin Hood, Maid Marian, Little John, Friar Tuck, Much the Miller's Son.
- **`6 Hand Slots`:** Clean hand layering with equipment items anchored to weapon/tool coordinate bounds.
- **Gas-Free Off-Chain Gameplay:** Verification algorithms (Dice, Archery, Target Practice) execute deterministically via pure Solidity math or JavaScript rendering mirrors with zero gas costs.

---
"""

def build_section_9():
    return r"""## 9. The Sherwood Astronomical Calendar & World Events Engine

### 1. Sherwood Astronomical Calendar:
The perpetual Sherwood Calendar runs on an autonomous 365-day astronomical cycle:
- **12 Months × 30 Days (Days 1–360):** Regular gameplay and monthly Castle Infiltrations.
- **5 Intercalary Solstice Days (Days 361–365):** The Grand Solstice Vault Heist tournament.
- **First-Month Handshake:** Day 1 begins at `GENESIS_TIME`, with zero pre-mine or retroactive active-Hood requirements.

### 2. Zero-Keeper World Event Synchronization (`syncWorldEvents`):
```solidity
enum ActionKind { CASTLE, TAX_TRAIN, JUBILEE }

struct EventConfig {
    bool exists;
    ActionKind kind;
    uint32 eventYear;
    uint64 startTime;
    uint64 endTime;
    uint32 cap;
}

mapping(uint256 => EventConfig) public events;
uint256 public nextBossThreshold = 150_000;
uint64 public bossCooldownEndsAt;
bool public taxTrainActive;
uint256 public currentTaxTrainEventId;

function syncWorldEvents() public {
    uint256 elapsed = block.timestamp - GENESIS_TIME;
    uint32 year = uint32(elapsed / 365 days) + 1;
    uint256 day = (elapsed % 365 days) / 1 days;
    uint32 mEpoch = uint32(elapsed / 365 days) * 12 + uint32(day < 360 ? day / 30 : 11);
    
    // 1. Monthly Castle Event (Days 28-30 of Months 1-11; indices 27..29)
    if (day < 330 && (day % 30) >= 27) {
        uint256 castleEventId = 1_000_000 + mEpoch;
        if (!events[castleEventId].exists) {
            uint64 mStart = uint64(GENESIS_TIME + (mEpoch / 12) * 365 days + (mEpoch % 12) * 30 days + 27 days);
            events[castleEventId] = EventConfig(true, ActionKind.CASTLE, year, mStart, mStart + 3 days, 5_000);
        }
    }
    
    // 2. Annual Solstice Championship (Days 359-365; indices 358..364)
    if (day >= 358) {
        uint256 solsticeId = 2_000_000 + year;
        if (!events[solsticeId].exists) {
            uint64 sStart = uint64(GENESIS_TIME + (year - 1) * 365 days + 358 days);
            events[solsticeId] = EventConfig(true, ActionKind.CASTLE /* placeholder config */, year, sStart, sStart + 7 days, 10_000);
        }
    }
    
    // 3. Sherwood Jubilee (Days 351-357 of Years 5, 10, 15, 20, 25; indices 350..356)
    if (year % 5 == 0 && year <= 25 && day >= 350 && day <= 356) {
        uint256 jubileeId = 3_000_000 + year;
        if (!events[jubileeId].exists) {
            uint64 jStart = uint64(GENESIS_TIME + (year - 1) * 365 days + 350 days);
            events[jubileeId] = EventConfig(true, ActionKind.JUBILEE, year, jStart, jStart + 7 days, 25_000);
        }
    }
    
    // 4. Tax Train World Boss (Economy-driven threshold)
    if (!taxTrainActive && block.timestamp >= bossCooldownEndsAt) {
        if (treasuresContract.cumulativeGoldBurned() >= nextBossThreshold) {
            bool jubileeYear = (year % 5 == 0 && year <= 25);
            uint256 protectedStart = jubileeYear ? 350 : 358;
            bool overlapsFestival = (day + 7 >= protectedStart);
            if (!overlapsFestival) {
                taxTrainActive = true;
                currentTaxTrainEventId = 4_000_000 + block.timestamp;
                events[currentTaxTrainEventId] = EventConfig(true, ActionKind.TAX_TRAIN, year, uint64(block.timestamp), uint64(block.timestamp + 7 days), 25_000);
            }
        }
    }
}
```

### 3. Unified Reusable `ActionRequest` Engine & Attempt Accounting (HQ-EVT-003):
```solidity
struct CombatSnapshot {
    uint8 atk;
    uint8 def;
    uint8 stealth;
    uint16 critBps;
    uint16 goldBonusBps;
    uint16 economicRewardBps;
    bool initialFatigue;
}

struct ActionRequest {
    uint256 hoodId;
    uint256 eventId;
    uint64 targetBlock;
    ActionKind kind;
    uint8 sector;
    CombatSnapshot snapshot;
}

mapping(uint256 => ActionRequest) public actionRequests;
mapping(uint256 => mapping(uint256 => uint256)) public hoodContribution; // eventId => hoodId => points
mapping(uint256 => uint256) public totalContribution;
mapping(uint256 => mapping(uint256 => bool)) public eventEntitlementOpen;

mapping(uint256 => mapping(uint256 => uint8)) public castleManeuversUsed; // eventId => hoodId => count (max 5)
mapping(uint256 => mapping(uint256 => uint8)) public jubileeManeuversUsed; // eventId => hoodId => count (max 5)
mapping(uint256 => mapping(uint256 => uint32)) public taxTrainLastAttackDay; // eventId => hoodId => day
mapping(uint256 => uint256) public castleBreachPoints;
mapping(uint256 => bool) public castleBreached;

function _consumeEventAttempt(uint256 hoodId, uint256 eventId, ActionKind kind) internal {
    if (kind == ActionKind.CASTLE) {
        require(castleManeuversUsed[eventId][hoodId] < 5, "Exceeds 5 Castle maneuvers");
        castleManeuversUsed[eventId][hoodId]++;
    } else if (kind == ActionKind.JUBILEE) {
        require(jubileeManeuversUsed[eventId][hoodId] < 5, "Exceeds 5 Jubilee maneuvers");
        jubileeManeuversUsed[eventId][hoodId]++;
    } else if (kind == ActionKind.TAX_TRAIN) {
        require(taxTrainLastAttackDay[eventId][hoodId] < currentUtcDay(), "Already attacked Tax Train today");
        taxTrainLastAttackDay[eventId][hoodId] = currentUtcDay();
    }
}

function requestActionEvent(
    uint256 hoodId,
    uint256 eventId,
    ActionKind kind,
    uint8 sector
) external returns (uint256 requestId) {
    syncWorldEvents();
    require(events[eventId].exists, "Event does not exist");
    require(events[eventId].kind == kind, "Kind mismatch: Solstice uses dedicated tournament methods");
    require(sector <= 4, "Invalid sector");
    require(msg.sender == hoodContract.ownerOf(hoodId) || hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
    require(!hoodContract.economicActionsPaused(), "Paused");
    require(hoodContract.heroSeed(hoodId) != bytes32(0), "Seed not finalized");
    require(block.timestamp >= events[eventId].startTime && block.timestamp <= events[eventId].endTime - 1 hours, "Action cutoff reached");
    
    _consumeEventAttempt(hoodId, eventId, kind);
    
    CombatSnapshot memory snap = captureCombatSnapshot(hoodId);
    requestId = ++nonce;
    uint64 target = uint64(ArbSys(address(0x64)).arbBlockNumber() + 2);
    
    actionRequests[requestId] = ActionRequest(hoodId, eventId, target, kind, sector, snap);
    hoodContract.incrementPendingGameplay(hoodId, 1);
    pendingRequestsByEngine[address(this)]++;
    emit ActionRequested(requestId, hoodId, eventId, kind);
}

function resolveActionEvent(uint256 requestId) external nonReentrant {
    ActionRequest memory req = actionRequests[requestId];
    require(req.targetBlock > 0, "Non-existent request");
    
    uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
    require(currentBlock > req.targetBlock, "Target not reached");
    
    delete actionRequests[requestId];
    hoodContract.decrementPendingGameplay(req.hoodId, 1);
    pendingRequestsByEngine[address(this)]--;
    
    if (currentBlock <= req.targetBlock + 256 && block.timestamp <= events[req.eventId].endTime + 2 hours) {
        bytes32 entropy = ArbSys(address(0x64)).arbBlockHash(req.targetBlock);
        uint256 points = _computeEventPoints(req, entropy);
        
        if (points > 0) {
            hoodContribution[req.eventId][req.hoodId] += points;
            totalContribution[req.eventId] += points;
            
            if (req.kind == ActionKind.CASTLE) {
                castleBreachPoints[req.eventId] += points;
                uint32 mEpoch = uint32(req.eventId - 1_000_000);
                if (castleBreachPoints[req.eventId] >= getBreachTarget(mEpoch)) {
                    castleBreached[req.eventId] = true;
                }
            }
            
            if (!eventEntitlementOpen[req.eventId][req.hoodId]) {
                eventEntitlementOpen[req.eventId][req.hoodId] = true;
                hoodContract.incrementPendingEventEntitlement(req.hoodId);
            }
            
            if (req.kind == ActionKind.JUBILEE) {
                _updateJubileeTop5(req.eventId, req.hoodId, hoodContribution[req.eventId][req.hoodId]);
            }
        }
        emit ActionResolved(requestId, req.hoodId, req.eventId, points);
    } else {
        emit ActionResolved(requestId, req.hoodId, req.eventId, 0);
    }
}
```

### 4. Bounded $O(5)$ Jubilee Top-5 Leaderboard (Per-Event Scoped - HQ-EVT-006):
```solidity
mapping(uint256 => uint256[5]) public jubileeTopHood;
mapping(uint256 => uint256[5]) public jubileeTopScore;

function _updateJubileeTop5(uint256 eventId, uint256 hoodId, uint256 newCumulativeScore) internal {
    int8 existingIndex = -1;
    for (uint8 i = 0; i < 5; i++) {
        if (jubileeTopHood[eventId][i] == hoodId) {
            existingIndex = int8(i);
            break;
        }
    }
    
    if (existingIndex >= 0) {
        jubileeTopScore[eventId][uint8(existingIndex)] = newCumulativeScore;
    } else {
        uint256 fifthScore = jubileeTopScore[eventId][4];
        uint256 fifthHood = jubileeTopHood[eventId][4];
        // Handles fifth-place ties strictly in favor of lower Hood ID
        if (newCumulativeScore > fifthScore || (newCumulativeScore == fifthScore && hoodId < fifthHood)) {
            jubileeTopHood[eventId][4] = hoodId;
            jubileeTopScore[eventId][4] = newCumulativeScore;
        }
    }
    
    // Sort top 5 descending in O(5)
    for (uint8 i = 0; i < 5; i++) {
        for (uint8 j = i + 1; j < 5; j++) {
            if (jubileeTopScore[eventId][j] > jubileeTopScore[eventId][i] || 
               (jubileeTopScore[eventId][j] == jubileeTopScore[eventId][i] && jubileeTopHood[eventId][j] < jubileeTopHood[eventId][i] && jubileeTopHood[eventId][j] != 0)) {
                uint256 sTemp = jubileeTopScore[eventId][i];
                uint256 hTemp = jubileeTopHood[eventId][i];
                jubileeTopScore[eventId][i] = jubileeTopScore[eventId][j];
                jubileeTopHood[eventId][i] = jubileeTopHood[eventId][j];
                jubileeTopScore[eventId][j] = sTemp;
                jubileeTopHood[eventId][j] = hTemp;
            }
        }
    }
}
```

### 5. Executable Solstice Championship (Event-Scoped & Expirable - HQ-EVT-004):
```solidity
struct SolsticeCommitment {
    bytes32 secretHash;
    uint32 eventYear;
    uint64 targetBlock;
    uint8 maneuverIndex; // 0..4
    bool active;
}

mapping(uint256 => mapping(uint256 => SolsticeCommitment)) public solsticeCommitments;
mapping(uint256 => mapping(uint256 => uint256)) public solsticeRenown;
mapping(uint256 => mapping(uint256 => uint8)) public currentSolsticeManeuver;
mapping(uint256 => uint256) public solsticeLeaderHood;
mapping(uint256 => uint256) public solsticeLeaderScore;

function commitSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secretHash, uint8 maneuverIndex) external returns (uint64 target) {
    syncWorldEvents();
    uint32 year = uint32(eventId - 2_000_000);
    uint64 sStart = uint64(GENESIS_TIME + (year - 1) * 365 days + 358 days);
    require(block.timestamp >= sStart && block.timestamp <= sStart + 7 days - 1 hours, "Action cutoff reached");
    require(msg.sender == hoodContract.ownerOf(hoodId), "Owner only");
    require(!hoodContract.economicActionsPaused(), "Paused");
    require(hoodContract.heroSeed(hoodId) != bytes32(0), "Seed not finalized");
    require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
    require(!solsticeCommitments[eventId][hoodId].active, "Prior commitment unresolved");
    require(maneuverIndex == currentSolsticeManeuver[eventId][hoodId], "Out of sequence maneuver");
    require(maneuverIndex < 5, "All 5 maneuvers completed");
    
    target = uint64(ArbSys(address(0x64)).arbBlockNumber() + 2);
    solsticeCommitments[eventId][hoodId] = SolsticeCommitment(secretHash, year, target, maneuverIndex, true);
    hoodContract.setSolsticeLock(hoodId, true);
    pendingRequestsByEngine[address(this)]++;
    emit SolsticeManeuverCommitted(hoodId, maneuverIndex, target);
}

function revealSolsticeManeuver(uint256 eventId, uint256 hoodId, bytes32 secret) external nonReentrant {
    SolsticeCommitment memory sc = solsticeCommitments[eventId][hoodId];
    require(sc.active, "No active commitment");
    
    uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
    require(currentBlock > sc.targetBlock, "Target block not reached");
    require(keccak256(abi.encode(secret, hoodId, sc.eventYear, sc.maneuverIndex, address(this), block.chainid)) == sc.secretHash, "Invalid secret");
    
    delete solsticeCommitments[eventId][hoodId];
    hoodContract.setSolsticeLock(hoodId, false);
    pendingRequestsByEngine[address(this)]--;
    currentSolsticeManeuver[eventId][hoodId]++;
    
    uint64 sEnd = uint64(GENESIS_TIME + (sc.eventYear - 1) * 365 days + 365 days);
    if (currentBlock <= sc.targetBlock + 256 && block.timestamp <= sEnd + 2 hours) {
        bytes32 entropy = keccak256(abi.encodePacked(
            ArbSys(address(0x64)).arbBlockHash(sc.targetBlock),
            secret,
            hoodId,
            sc.eventYear,
            sc.maneuverIndex,
            block.chainid
        ));
        uint256 points = 50 + (uint256(entropy) % 51);
        
        // Both hoodContribution and solsticeRenown are accrued so Gold and trophies settle identically
        hoodContribution[eventId][hoodId] += points;
        solsticeRenown[eventId][hoodId] += points;
        totalContribution[eventId] += points;
        
        if (!eventEntitlementOpen[eventId][hoodId]) {
            eventEntitlementOpen[eventId][hoodId] = true;
            hoodContract.incrementPendingEventEntitlement(hoodId);
        }
        
        if (solsticeRenown[eventId][hoodId] > solsticeLeaderScore[eventId]) {
            solsticeLeaderScore[eventId] = solsticeRenown[eventId][hoodId];
            solsticeLeaderHood[eventId] = hoodId;
        }
        emit SolsticeManeuverRevealed(hoodId, sc.maneuverIndex, points);
    } else {
        emit SolsticeManeuverRevealed(hoodId, sc.maneuverIndex, 0);
    }
}

function expireSolsticeManeuver(uint256 eventId, uint256 hoodId) external {
    SolsticeCommitment memory sc = solsticeCommitments[eventId][hoodId];
    require(sc.active, "No active commitment");
    uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
    uint64 sEnd = uint64(GENESIS_TIME + (sc.eventYear - 1) * 365 days + 365 days);
    require(currentBlock > sc.targetBlock + 256 || block.timestamp > sEnd + 2 hours, "Window still open");
    
    delete solsticeCommitments[eventId][hoodId];
    hoodContract.setSolsticeLock(hoodId, false);
    pendingRequestsByEngine[address(this)]--;
    currentSolsticeManeuver[eventId][hoodId]++;
    emit SolsticeManeuverExpired(eventId, hoodId, sc.maneuverIndex);
}
```

### 6. Event Finalization, Trophy Reservation & Settlement Lifecycle (HQ-EVT-007, HQ-EVT-008):
```solidity
struct EventRecord {
    uint256 finalBudget;
    uint256 totalContribution;
    uint256 claimDeadline;
    uint256 claimedTotal;
    bool finalized;
}

mapping(uint256 => EventRecord) public eventRecords;
mapping(uint256 => mapping(uint256 => bool)) public eventClaimed;
mapping(uint256 => mapping(uint256 => mapping(uint256 => bool))) public eventTrophyEntitlement;

mapping(uint256 => bool) public eventLiabilityOpen;
mapping(uint256 => bool) public eventGoldSettled;
mapping(uint256 => uint8) public eventTrophiesOutstanding;

function _tryCloseEventLiability(uint256 eventId) internal {
    if (eventLiabilityOpen[eventId] && eventGoldSettled[eventId] && eventTrophiesOutstanding[eventId] == 0) {
        eventLiabilityOpen[eventId] = false;
        if (outstandingEventLiabilitiesByEngine[address(this)] > 0) {
            outstandingEventLiabilitiesByEngine[address(this)]--;
        }
        emit EventLiabilityClosed(eventId);
    }
}

function finalizeEvent(uint256 eventId) external nonReentrant {
    syncWorldEvents();
    require(events[eventId].exists, "Event does not exist");
    require(block.timestamp > events[eventId].endTime + 2 hours, "Grace period active");
    EventRecord storage e = eventRecords[eventId];
    require(!e.finalized, "Already finalized");
    
    e.totalContribution = totalContribution[eventId];
    
    bool payableEvent = true;
    if (events[eventId].kind == ActionKind.CASTLE && !castleBreached[eventId]) {
        payableEvent = false;
    }
    
    if (e.totalContribution == 0 || !payableEvent) {
        e.finalBudget = 0;
        eventGoldSettled[eventId] = true;
    } else {
        e.finalBudget = treasuresContract.reserveEventBudget(eventId, events[eventId].cap);
        eventLiabilityOpen[eventId] = true;
        outstandingEventLiabilitiesByEngine[address(this)]++;
        _reserveEventTrophies(eventId);
    }
    
    e.finalized = true;
    e.claimDeadline = block.timestamp + 90 days;
    
    if (events[eventId].kind == ActionKind.TAX_TRAIN) {
        taxTrainActive = false;
        bossCooldownEndsAt = uint64(block.timestamp + 14 days);
        nextBossThreshold = treasuresContract.cumulativeGoldBurned() + 150_000;
    }
    
    _tryCloseEventLiability(eventId);
    emit EventFinalized(eventId, e.finalBudget, e.totalContribution);
}

function _reserveEventTrophies(uint256 eventId) internal {
    EventConfig memory cfg = events[eventId];
    if (eventId >= 2_000_000 && eventId < 3_000_000 && cfg.eventYear <= 20) {
        uint256 leader = solsticeLeaderHood[eventId];
        if (leader != 0) {
            treasuresContract.reserveEventTrophy(eventId, GOLDEN_ARROW, 1);
            eventTrophyEntitlement[eventId][leader][GOLDEN_ARROW] = true;
            eventTrophiesOutstanding[eventId]++;
        }
    } else if (cfg.kind == ActionKind.JUBILEE) {
        uint256 champion = jubileeTopHood[eventId][0];
        if (champion != 0) {
            treasuresContract.reserveEventTrophy(eventId, GOLDEN_ARROW, 1);
            eventTrophyEntitlement[eventId][champion][GOLDEN_ARROW] = true;
            eventTrophiesOutstanding[eventId]++;
        }
        for (uint8 i = 0; i < 5; i++) {
            uint256 hood = jubileeTopHood[eventId][i];
            if (hood != 0) {
                treasuresContract.reserveEventTrophy(eventId, FRIARS_CORNUCOPIA, 1);
                eventTrophyEntitlement[eventId][hood][FRIARS_CORNUCOPIA] = true;
                eventTrophiesOutstanding[eventId]++;
            }
        }
    }
}

function claimEventReward(uint256 eventId, uint256 hoodId, address recipient) external nonReentrant {
    require(recipient != address(0), "Invalid recipient");
    address owner = hoodContract.ownerOf(hoodId);
    if (msg.sender != owner) {
        require(hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(recipient == owner, "Delegates can only claim to Hood owner");
    }
    
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp < e.claimDeadline, "Claim window expired");
    require(!eventClaimed[eventId][hoodId], "Already claimed");
    
    uint256 userContribution = hoodContribution[eventId][hoodId];
    require(userContribution > 0, "Zero contribution");
    
    eventClaimed[eventId][hoodId] = true;
    eventEntitlementOpen[eventId][hoodId] = false;
    hoodContract.decrementPendingEventEntitlement(hoodId);
    
    uint256 reward = (e.finalBudget * userContribution) / e.totalContribution;
    e.claimedTotal += reward;
    
    treasuresContract.mintReservedEventGold(recipient, eventId, reward);
    
    if (e.claimedTotal == e.finalBudget) {
        eventGoldSettled[eventId] = true;
        _tryCloseEventLiability(eventId);
    }
    emit EventRewardClaimed(eventId, hoodId, recipient, reward);
}

function claimEventTrophy(uint256 eventId, uint256 hoodId, uint256 itemId, address recipient) external nonReentrant {
    require(recipient != address(0), "Invalid recipient");
    require(msg.sender == hoodContract.ownerOf(hoodId), "Not owner");
    require(eventTrophyEntitlement[eventId][hoodId][itemId], "No trophy entitlement");
    
    EventRecord storage e = eventRecords[eventId];
    require(block.timestamp < e.claimDeadline, "Claim deadline expired");
    
    delete eventTrophyEntitlement[eventId][hoodId][itemId];
    eventTrophiesOutstanding[eventId]--;
    
    treasuresContract.mintReservedTrophy(eventId, recipient, itemId);
    _tryCloseEventLiability(eventId);
    emit EventTrophyClaimed(eventId, hoodId, itemId, recipient);
}

function forfeitUnclaimedTrophy(uint256 eventId, uint256 hoodId, uint256 itemId) external nonReentrant {
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp >= e.claimDeadline, "Claim deadline active");
    require(eventTrophyEntitlement[eventId][hoodId][itemId], "No trophy entitlement");
    
    delete eventTrophyEntitlement[eventId][hoodId][itemId];
    eventTrophiesOutstanding[eventId]--;
    
    treasuresContract.forfeitReservedTrophy(eventId, itemId);
    _tryCloseEventLiability(eventId);
    emit TrophyForfeited(eventId, hoodId, itemId);
}

function expireHoodEventParticipation(uint256 eventId, uint256 hoodId) external {
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp >= e.claimDeadline, "Claim window active");
    require(eventEntitlementOpen[eventId][hoodId], "No open entitlement");
    
    eventEntitlementOpen[eventId][hoodId] = false;
    hoodContract.decrementPendingEventEntitlement(hoodId);
    emit HoodParticipationExpired(eventId, hoodId);
}

function refundUnclaimedEventBudget(uint256 eventId) external {
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp >= e.claimDeadline, "Claim window active");
    require(!eventGoldSettled[eventId], "Gold already settled");
    
    uint256 unclaimed = e.finalBudget - e.claimedTotal;
    e.claimedTotal = e.finalBudget;
    eventGoldSettled[eventId] = true;
    
    if (unclaimed > 0) {
        treasuresContract.refundEventBudget(eventId, unclaimed);
    }
    
    _tryCloseEventLiability(eventId);
    emit UnclaimedBudgetRefunded(eventId, unclaimed);
}
```

---
"""

def build_section_10():
    return r"""## 10. Bounded-Emission Governance & Expansion Blueprint

```mermaid
flowchart TD
    subgraph Core ["The Permanent Core (Immutable Invariants)"]
        Vault["HoodQuestTreasures.sol<br>• ID 1 = CORE_CURRENCY<br>• IDs 2-20 = CORE_ONLY<br>• IDs 21+ = EXPANSION_REGISTRY<br>• rewardExpansionGold() sole Gold entry point"]
    end

    subgraph Expansion ["Year 2+ Expansions (48-Hour Timelock)"]
        R1["New Immutable Raid Module"] -->|"48-Hour Public Timelock"| Vault
        R1 -->|"Enforced at Registration: allocatedCap <= 25,000"| Vault
    end
```

### 1. Item Permissions & Single Gold Faucet:
- `ID 1` is `CORE_CURRENCY`; `IDs 2–20` are permanently `CORE_ONLY`.
- Expansion modules have zero generic mint authority. The sole authorized Gold faucet for modules is `rewardExpansionGold(player, amount)`.
- For `IDs 21+`, modules require timelocked registration via `registerExpansionItem(id, module, supplyMode, cap)`.

### 2. Authorization-Time Cap Check, Revocation Solvency & Daily Module Mint State Machine (HQ-GOV-006):
```solidity
uint256 public constant MAX_EXPANSION_DAILY_CAP = 25_000;
uint256 public totalAllocatedDailyCap;
mapping(address => uint256) public moduleDailyCap;
mapping(address => bool) public isModuleAuthorized;
mapping(address => uint32) public moduleMintDay;
mapping(address => uint256) public moduleMintedToday;

function setModuleAuthorization(address module, uint256 dailyCap, bool authorized) external onlyTimelock {
    if (authorized && !isModuleAuthorized[module]) {
        require(dailyCap > 0, "Cap must be > 0");
        require(totalAllocatedDailyCap + dailyCap <= MAX_EXPANSION_DAILY_CAP, "Exceeds 25k daily cap");
        totalAllocatedDailyCap += dailyCap;
        moduleDailyCap[module] = dailyCap;
        isModuleAuthorized[module] = true;
    } else if (!authorized && isModuleAuthorized[module]) {
        totalAllocatedDailyCap -= moduleDailyCap[module];
        moduleDailyCap[module] = 0;
        isModuleAuthorized[module] = false;
    }
    emit ModuleAuthorizationChanged(module, authorized, dailyCap);
}

function rewardExpansionGold(address to, uint256 amount) external nonReentrant {
    require(isModuleAuthorized[msg.sender], "Unauthorized module");
    require(to != address(0), "Invalid recipient");
    
    uint32 today = uint32(block.timestamp / 1 days);
    if (today > moduleMintDay[msg.sender]) {
        moduleMintDay[msg.sender] = today;
        moduleMintedToday[msg.sender] = 0;
    }
    
    require(moduleMintedToday[msg.sender] + amount <= moduleDailyCap[msg.sender], "Exceeds daily module cap");
    moduleMintedToday[msg.sender] += amount;
    _mint(to, 1, amount, "");
    emit ExpansionGoldRewarded(msg.sender, to, amount);
}
```

### 3. OpenZeppelin TimelockController Deployment Configuration:
- **Delay:** `48 hours` (172,800 seconds).
- **Proposer:** Multi-signature governance wallet (`PROCEEDS_RECIPIENT`).
- **Executor:** Open permissionless execution (`address(0)` allows anyone to trigger an expired timelock proposal).
- **Admin:** The `TimelockController` contract is its own admin, preventing unilateral parameter bypasses.

---
"""

def build_section_11():
    return r"""## 11. Master Pre-Flight Audit & Verification Lifecycle Matrix

### Engineering Verification Lifecycle:
All audit items must be tracked across the formal verification lifecycle:
`Specified` -> `Implemented` -> `Unit Tested` -> `Fuzz Tested` -> `Invariant Tested` -> `Testnet Verified` -> `Independently Reviewed` -> `Mainnet Ready`.

| Security Domain | Vulnerability / Threat | Proposed On-Chain Defense Mechanism | Engineering Status |
| :--- | :--- | :--- | :--- |
| **Bazaar Gold Custody** | Burn/mint in Bazaar creating insolvency risk | **Atomic Fee Burn & Escrow:** Burn fee only; transfer proceeds into Bazaar custody; withdrawal transfers held tokens. | `[Specified]` |
| **Aggregate ERC-1155 Custody** | Invariant INV-15 failing on fungible items | **boundCount Mapping:** Tracks total bound per itemId; verifies Vault balance == boundCount[itemId]. | `[Specified]` |
| **Supply Mode Enforcement** | Circulating caps treated as lifetime caps | **SupplyMode Enum:** Tracks MAX_LIFETIME vs MAX_CIRCULATING using OpenZeppelin ERC1155Supply. | `[Specified]` |
| **Gilded Bow 250 Drop Cap** | Forge crafters exhausting drop slots | **Split Cap Enforcement:** reserveItem checks droppedGildedBows < 250; craft checks forgedGildedBows < 750. | `[Specified]` |
| **Solstice Bypass Guard** | Solstice requests falling into shared action path | **Kind Validation:** Solstice excluded from shared ActionKind; requires 5-maneuver commit-reveal. | `[Specified]` |
| **Solstice Renown Accrual** | Renown tracked without hoodContribution | **Dual Contribution Accrual:** Accrues both hoodContribution and solsticeRenown on reveal. | `[Specified]` |
| **Multi-Unit Drop Solvency** | Single reservation on multi-item drops | **Requested Amount API:** reserveItem takes requestedAmount and grants up to available headroom. | `[Specified]` |
| **Heist Claim Solvency** | Incrementing counter on empty bundles | **Post-Reservation Non-Zero Check:** finalBundleNonZero computed after all drops/skips. | `[Specified]` |
| **Event Liability Invariant** | Repeated decrements on zero refunds | **Idempotent Liability Closure:** _tryCloseEventLiability decrements engine counter once when all obligations hit zero. | `[Specified]` |
| **Trophy Event Scoping** | Global pooling of event trophy reservations | **eventTrophyReserved Mapping:** Keyed by engine, eventId, and itemId. | `[Specified]` |
| **World State Persistence** | Raid upgrade resetting 25-year calendar | **HoodQuestWorldState Contract:** Canonical world timeline decoupled from combat engines. | `[Specified]` |
| **Canonical Core Gating** | Pending event counts fragmented by engine | **Core Token Counters:** pendingGameplay, pendingEvent, pendingReward tracked directly in HoodQuest core. | `[Specified]` |

---
"""

def build_section_12():
    return r"""## 12. Mainnet Acceptance Test & Invariant Specification

The following 18 invariants must be mathematically verified in Foundry before protocol deployment to **Robinhood Testnet (Chain ID 46630)**:

### INV-1: Hood Token Supply & ID Invariant
- `totalHoodsMinted <= 10,000`.
- All minted token IDs satisfy `1 <= id <= 10,000`. Token ID `0` is strictly unmintable.

### INV-2: Mythic Grail Lifetime Mint Ceilings
- The Golden Arrow (#4) satisfies `lifetimeMinted[4] + reservedUnclaimed[4] + forfeitedGrails[4] <= 25`.
- Friar's Cornucopia (#9) satisfies `lifetimeMinted[9] + reservedUnclaimed[9] + forfeitedGrails[9] <= 25`.

### INV-3: Companion Genesis Parity & Adoption Limit
- For any Hood token ID, `genesisAdoptionUsed[hoodId]` is set to `true` at most once.
- `totalSupply() <= 10,000` with species sub-caps: Hounds `1..4000`, Falcons `4001..7000`, Owls `7001..10000`.

### INV-4: Identity-Bound Temporal Tracking
- `baseHeistsUsed`, `bonusHeistsUsed`, `lastHeistDay`, `rationsUntil`, and `effectiveBiologicalAge` are permanently bound to `tokenId`.
- Transferring an NFT does not reset any daily allowance or cooldown.

### INV-5: Starvation Economic Multiplier Clamp
- When `rationsUntil[tokenId] < block.timestamp`, `effectiveEconomicRewardBps(tokenId) == 2500` (25% yield clamp).

### INV-6: Slumbering Action Prohibition
- While `isSlumbering(tokenId) == true`, calls to `requestHeistBatch`, `requestActionEvent`, `commitSolsticeManeuver`, `feed`, and `soloForage` strictly revert.

### INV-7: Bounded Expansion Emission Ceiling
- `totalAllocatedDailyCap <= 25,000 Gold/day`.
- Daily module emissions cannot exceed `moduleDailyCap[module]`.

### INV-8: Armory Vault Custody Integrity
- For all equippable items `itemId`, `treasuresContract.balanceOf(HoodQuestVault, itemId) == boundCount[itemId]`.

### INV-9: Global Rebate Reserve Solvency
- `rebateReserve` is credited with 25% of burned Gold; 75% is permanently burned.
- `rebateReserve >= sum(eventGoldReserved)`.

### INV-10: Delayed Entropy Terminal State Guarantee
- Randomness requests older than 256 blocks resolve safely through deterministic fallback logic with zero reversions.

### INV-11: Mixed Stamina Batch Roll Classification
- In any heist batch of size $N$, rolls $i < \text{baseConsumed}$ are base rolls; rolls $i \ge \text{baseConsumed}$ are bonus rolls.
- Greenwood Elixirs drop strictly on base rolls.

### INV-12: Single Pending Heist Batch Invariant
- At most 1 pending heist batch can exist per Hood ID (`pendingNormalHeist[tokenId] == false` required to request).

### INV-13: Delegate Asset Non-Redirection & Inventory Spending
- `claimHeistRewards` called by a delegate transfers rewards strictly to `ownerOf(hoodId)`.
- Delegates calling `feed` or `useElixir` burn items strictly from their own inventory.

### INV-14: Scarce-Reward Reservation Solvency
- `treasuresContract.reservedUnclaimed(itemId) >= sum(unclaimedHeistRewards[hoodId].item)`.

### INV-15: Aggregate ERC-1155 Vault Custody
- Gear equipped by Hoods is held in aggregate custody by the Core contract with exact reverse slot accounting.

### INV-16: Per-Slot Unequip Request Isolation
- Initiating unequip on slot $S$ affects only slot $S$ and matures after 24 hours.

### INV-17: Bazaar Escrow Solvency & Liability Coverage
- `treasuresContract.balanceOf(bazaarContract, 1) >= sum(bazaarProceedsEscrow)`.
- `HoodQuest.balanceOf(bazaarContract) == activeListingTokenIds.length`.

### INV-18: Gilded Bow Split Cap Invariant
- `forgedGildedBows <= 750` and `droppedGildedBows + dropReservedGildedBows <= 250`.
- `lifetimeMinted[3] <= 1,000`.

---
"""

def build_section_13():
    return r"""## 13. Normative Requirements Registry

> [!IMPORTANT]
> **Normative Registry Self-Consistency Invariant:**
> A requirement ID marked `[Present]` is valid **if and only if** its full executable specification (constants, structs, state mappings, and complete function logic) exists in Sections 2 through 10. Registry-only statements do not satisfy requirements.

| Requirement ID | Canonical Domain | Normative Invariant Summary | Implementation Cross-Reference |
| :--- | :--- | :--- | :--- |
| **HQ-CORE-001** | Immutable Cap | Maximum Hood supply strictly immutable at 10,000; IDs 1..10,000. | `[Present - Section 2]` |
| **HQ-CORE-002** | Zero Pre-Mine | All Hoods minted via public payable `mintHoods`; zero admin mint. | `[Present - Section 2]` |
| **HQ-CORE-003** | Receiver Hooks | HoodQuest inherits `ERC1155Holder` and `IERC721Receiver` for escrow custody. | `[Present - Section 2]` |
| **HQ-CORE-004** | Core Gating Counters | `pendingGameplay`, `pendingEventEntitlement`, `pendingHeistReward` tracked in Core. | `[Present - Section 2]` |
| **HQ-CORE-005** | Pre-Sale Gate | `canList` verifies canonical core counters and armory locks. | `[Present - Section 2]` |
| **HQ-CORE-006** | Bazaar Transfer Mode | Handshake prevents 24h buyer lock on cancel; enforces lock on purchase. | `[Present - Section 2]` |
| **HQ-CORE-007** | Delegate Epochs | Wallet transfers increment `delegateEpoch` invalidating all delegates in O(1). | `[Present - Section 2]` |
| **HQ-CORE-008** | Caller Inventory | Delegates spending baskets or elixirs burn strictly from their own balance. | `[Present - Section 2]` |
| **HQ-CORE-009** | Biological Clock | Effective age advances only when awake; slumber pauses age with zero gas. | `[Present - Section 7]` |
| **HQ-CORE-010** | Devotion Ladder | Awake time awards +2% (30d), +4% (90d), +6% (180d), +10% (360d Gold cap). | `[Present - Section 7]` |
| **HQ-CORE-011** | Fresh Mint Init | Sets `mintTimestamp`, `lastCareDay = day - 1`, `rationsUntil = now + 7 days`. | `[Present - Section 2]` |
| **HQ-CORE-012** | Deposit Guards | Bazaar and Vault revert unsolicited direct ERC-721 transfers. | `[Present - Section 2]` |
| **HQ-TREAS-001** | Currency ID | Royal Gold Sovereign is permanently Token ID 1. | `[Present - Section 2]` |
| **HQ-TREAS-002** | Rebate Reserve | Burning Gold permanently destroys 75%; credits 25% to `rebateReserve`. | `[Present - Section 2]` |
| **HQ-TREAS-003** | Soulbound Materials | Sherwood Yew (#16) and Nottingham Iron (#17) are non-transferable proof-of-play. | `[Present - Section 2]` |
| **HQ-TREAS-004** | Three-Tier Permissions | Explicit `activeRaidEngine`, `resolverApproved`, and `settlementApproved`. | `[Present - Section 2]` |
| **HQ-TREAS-005** | Gilded Split Cap | Gilded Bow hard capped at 750 Forge Mints + 250 Drop Mints (1,000 total). | `[Present - Section 5]` |
| **HQ-TREAS-006** | Multi-Unit Reservations | `reserveItem` grants up to available capacity for batch drop solvency. | `[Present - Section 5]` |
| **HQ-TREAS-007** | Event Trophy Scoping | Trophy reservations tracked per engine, event, and item with forfeiture. | `[Present - Section 5]` |
| **HQ-TREAS-008** | Privilege Wrappers | Strict caller domain wrappers for adoption, forage, elixir, and bazaar settlement. | `[Present - Section 5]` |
| **HQ-ARM-001** | Equipment Custody | ERC-1155 vault custody verified via `boundCount[itemId] == balanceOf(Vault, itemId)`. | `[Present - Section 4]` |
| **HQ-ARM-002** | Unequip Notices | 24-hour maturation notice per slot; direct equip swapping is strictly prohibited. | `[Present - Section 4]` |
| **HQ-ARM-003** | Arrow Dependency | Equipping Golden Arrow requires equipped Bow; Bow cannot be unequipped while Arrow equipped. | `[Present - Section 4]` |
| **HQ-ARM-004** | Cornucopia Lock | 7-day minimum bind lock before Cornucopia unequip can be initiated. | `[Present - Section 4]` |
| **HQ-ARM-005** | Pet Bonding Lock | 12-hour minimum initial bond; 12-hour debond maturation notice. | `[Present - Section 4]` |
| **HQ-ARM-006** | Loadout Hash | 8-element typed hash verified at Bazaar settlement; `loadoutVersion` updated on all mutations. | `[Present - Section 4]` |
| **HQ-BAZ-001** | Trading Currency | Bazaar trades strictly in Gold Sovereigns (Token ID 1). | `[Present - Section 4]` |
| **HQ-BAZ-002** | Bazaar Custody | Bazaar holds buyer Gold in custody; burns 2.5% fee; seller withdraws held Gold (zero reminting). | `[Present - Section 4]` |
| **HQ-BAZ-003** | Pre-Sale Gate | `canList` verifies zero pending gameplay, unfinalized unequips/debonds, or unclaimed rewards. | `[Present - Section 4]` |
| **HQ-BAZ-004** | Discovery Arrays | Active listings tracked in swap-and-pop array with `activeListingIndexPlusOne` and 1..100 pagination. | `[Present - Section 4]` |
| **HQ-RNG-001** | Delayed L2 Entropy | Randomness requested at `targetBlock = arbBlock + 2`; resolved via `ArbSys(0x64).arbBlockHash`. | `[Present - Section 3]` |
| **HQ-RNG-002** | Heist Snapshot | Combat attributes, hunger, and fatigue snapshotted at request; resolution uses snapshot strictly. | `[Present - Section 3]` |
| **HQ-RNG-003** | Batch Stamina | Up to 5 heists per batch; returns `(baseCount, bonusCount)`; base rolls evaluated first. | `[Present - Section 3]` |
| **HQ-RNG-004** | Sequential Fatigue | Fatigue propagates roll-by-roll within a batch; at most 1 pending normal heist batch per Hood. | `[Present - Section 3]` |
| **HQ-RNG-005** | Domain Separation | 10 dedicated domain strings for Gold, Crit, Yew, Iron, Gilded, Common, Mead, Basket, Elixir. | `[Present - Section 3]` |
| **HQ-RNG-006** | Heist Fallback | Requests past 256 blocks evaluate base roll 1 through economic pipeline; 0 materials/rares. | `[Present - Section 3]` |
| **HQ-COMBAT-001**| Heist Combat Math | Power & Difficulty formulas with ATK, STEALTH / 2, and critical strike bonus. | `[Present - Section 3]` |
| **HQ-COMBAT-002**| Fatigue Generation | Mitigated damage > 20 generates fatigue affecting the subsequent roll. | `[Present - Section 3]` |
| **HQ-ECO-001**   | Fixed-Point Gold | Starvation and Gold-bonus carry evaluated with fixed-point `Math.mulDiv`. | `[Present - Section 3]` |
| **HQ-EVT-001** | Sherwood Calendar | 12 thirty-day months (Days 1–360) + 5 Solstice days (Days 361–365). | `[Present - Section 9]` |
| **HQ-EVT-002** | Persistent World State| Canonical world timeline held in `HoodQuestWorldState` across engine upgrades. | `[Present - Section 2]` |
| **HQ-EVT-003** | ActionRequest Engine | Shared state machine for Castle, Tax Train, and Jubilee with cutoff and grace periods. | `[Present - Section 9]` |
| **HQ-EVT-004** | Solstice Championship | 5-maneuver sequential commit-reveal tournament awarding annual Golden Arrow (Years 1–20). | `[Present - Section 9]` |
| **HQ-EVT-005** | Tax Train Boss | Activates on cumulative Gold burn threshold; 7-day battle; queues during Jubilee/Solstice. | `[Present - Section 9]` |
| **HQ-EVT-006** | Sherwood Jubilee | 5-year scheduled climax boss (Years 5, 10, 15, 20, 25); bounded O(5) leaderboard awards Cornucopias. | `[Present - Section 9]` |
| **HQ-EVT-007** | Idempotent Liabilities | `_tryCloseEventLiability` decrements engine liabilities once when all obligations hit zero. | `[Present - Section 9]` |
| **HQ-EVT-008** | Trophy Forfeiture | Unclaimed trophies expire after 90 days and are permanently forfeited (never reminted). | `[Present - Section 9]` |
| **HQ-COMP-001** | Genesis Adoption | 10,000 maximum Genesis companions; max 1 adoption per Hood lifetime. | `[Present - Section 2]` |
| **HQ-COMP-002** | Species Pricing | Hound (IDs 1–4k, 20 Gold); Falcon (IDs 4001–7k, 30 Gold); Owl (IDs 7001–10k, 40 Gold). | `[Present - Section 2]` |
| **HQ-COMP-003** | Pet Clock | Pet age advances only while bonded to awake Hood; derived from host biological age. | `[Present - Section 6]` |
| **HQ-COMP-004** | Bond Ranks | Ranks 1–5 derived from pet XP (0, 300, 900, 1800, 3650); grants DEF, Crit, Gold, Stealth perks. | `[Present - Section 6]` |
| **HQ-COMP-005** | Forage Accrual | Daily foraging rewards accrue to `pendingForageYew/Iron[hoodId]`; claimed by Hood owner. | `[Present - Section 6]` |
| **HQ-GOV-001** | Timelock Control | 48-hour delay on all governance actions and module authorizations. | `[Present - Section 10]` |
| **HQ-GOV-002** | Expansion Cap | Sum of all active expansion module daily mint caps cannot exceed 25,000 Gold/day. | `[Present - Section 10]` |
| **HQ-GOV-003** | Cap Revocation | Disabling an expansion module subtracts its cap; re-enabling verifies `allocatedCap <= 25,000`. | `[Present - Section 10]` |
| **HQ-GOV-004** | Two-Phase Raids | Retiring Raid engine loses request creation immediately; retains settlement until claims reach zero. | `[Present - Section 2]` |
| **HQ-GOV-005** | Renderer Fallback | Staticcall wrapped in assembly `returndatasize` bound; falls back to minimal JSON on failure. | `[Present - Section 2]` |
| **HQ-GOV-006** | Expansion Faucet | `rewardExpansionGold` state machine tracks daily module limits with UTC resets. | `[Present - Section 10]` |
"""

def generate_complete_blueprint():
    sections = [
        build_section_0(),
        build_section_1(),
        build_section_2(),
        build_section_3(),
        build_section_4(),
        build_section_5(),
        build_section_6(),
        build_section_7(),
        build_section_8(),
        build_section_9(),
        build_section_10(),
        build_section_11(),
        build_section_12(),
        build_section_13()
    ]
    return "\n".join(sections)

if __name__ == "__main__":
    content = generate_complete_blueprint()
    destinations = [
        "/home/arson/rhnftproject/HOODQUEST_MASTER_BLUEPRINT.md",
        "/mnt/c/Users/Eric/Desktop/HOODQUEST_MASTER_BLUEPRINT.md",
        "/mnt/c/Users/Eric/Downloads/HOODQUEST_MASTER_BLUEPRINT.md"
    ]
    for d in destinations:
        with open(d, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully wrote {d} ({len(content)} bytes, {len(content.splitlines())} lines)")
