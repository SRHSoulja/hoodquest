import os

def build_blueprint():
    content = """# HoodQuest (HQ): Production System Specification (Protocol Frozen V1.0)

A mathematically closed, executable smart contract specification for **HoodQuest (HQ)**, a 100% on-chain living companion RPG with zero backend servers, indexers, or relayers, deployed natively on **Robinhood Chain (Testnet Chain ID 46630, Mainnet Chain ID 4663)**.

- **Official Brand:** **HoodQuest**
- **Shorthand / Ticker:** **HQ**
- **Testnet Subdomain:** `rhtestnethq.gmgnrepeat.com`
- **Future Mainnet Subdomain:** `hq.gmgnrepeat.com`
- **Specification Release:** **Protocol Frozen V1.0 (Production-Ready Specification)**
- **Strict Target Notice:** Testing and deployment are strictly restricted to **Robinhood Testnet (46630)** and local Foundry test environments. Mainnet (4663) remains locked until full audit cycle completion.

---

## Table of Contents
1. [Core Vision & 25-Year Pillars](#1-core-vision--25-year-pillars)
2. [Smart Contract Topology & Security Architecture](#2-smart-contract-topology--security-architecture)
3. [The Calibrated 25-Year Economic Engine & Heist State Machine](#3-the-calibrated-25-year-economic-engine--heist-state-machine)
4. [The Armory Escrow Vault & Marketplace Shield](#4-the-armory-escrow-vault--marketplace-shield)
5. [Anti-Power-Creep Weapon, Combat Matrix & Blacksmith](#5-anti-power-creep-weapon-combat-matrix--blacksmith)
6. [Mother Meg's Rescue Post & Companion Sidecars](#6-mother-megs-rescue-post--companion-sidecars)
7. [The Upkeep, Slumber & Calibrated Devotion System](#7-the-upkeep-slumber--calibrated-devotion-system)
8. [Gas-Free On-Chain Minigames & Artisan Vector Art Pipeline](#8-gas-free-on-chain-minigames--artisan-vector-art-pipeline)
9. [The Sherwood Astronomical Calendar & World Events Engine](#9-the-sherwood-astronomical-calendar--world-events-engine)
10. [Bounded-Emission Governance & Expansion Blueprint](#10-bounded-emission-governance--expansion-blueprint)
11. [Master Pre-Flight Audit & Verification Lifecycle Matrix](#11-master-pre-flight-audit--verification-lifecycle-matrix)
12. [Mainnet Acceptance Test & Invariant Specification](#12-mainnet-acceptance-test--invariant-specification)

---

## 1. Core Vision & 25-Year Pillars

```mermaid
flowchart TD
    subgraph Pillars ["Core System Pillars"]
        P1["Living Pocket Companion<br>25 Active Years of Living Devotion"]
        P2["Pure On-Chain SVG<br>Solidity Direct Rendering & EIP-4906"]
        P3["Deflationary Gold Sink Engine<br>Rebate Reserve + Net 75% Permanent Burn"]
        P4["Armory Escrow Vault<br>Gear Bound to NFT; Zero Double-Listing"]
        P5["Anti-Power-Creep Covenant<br>Stat Ceilings & Split Forging/Drop Caps"]
        P6["Zero-Server World Engine<br>360+5 Solstice Calendar & ActionRequest Engine"]
        P7["Bounded-Emission Governance<br>Core Owns Limits; Timelocked Modules"]
    end
```

1. **"25 Years" Means 25 Years of Active Devotion:** Biological evolution is driven strictly by **effective wakefulness**. Slumber pauses the biological aging clock ($0 gas during sleep). For average players taking real-world breaks, reaching Legend status spans **35 to 50+ real-world calendar years**, creating a multi-generational digital heirloom.
2. **Decoupled Hero Age vs. Sherwood World Calendar:** Hero Biological Age (advancing only when cared for and awake) is strictly decoupled from the perpetual **Sherwood World Calendar** (an autonomous 365-day astronomical cycle of 12 thirty-day months plus 5 intercalary Solstice days running perpetually).
3. **100% On-Chain Autonomy:** Zero centralized servers, zero indexer dependencies, zero gas relayers. All visuals, stats, encounters, and loot rolls live directly in Solidity EVM bytecode.
4. **Capped Macro Economy:** Governed by an immutable maximum token supply (`MAX_HOOD_SUPPLY = 10,000`), token IDs strictly start at 1, and no admin mint or un-capped emission paths exist.
5. **Anti-Power-Creep Guarantee:** Early Genesis gear (2026) is never rendered obsolete. Statutory stat ceilings, split drop/forge caps, and horizontal combat archetypes protect player investments forever.
6. **Bounded-Emission Governance:** The developer has zero admin-mint capabilities. All expansions use a 48-hour public on-chain timelock and cannot exceed strict daily emission budgets.
7. **Identity-Bound Temporal Tracking:** All daily allowances, stamina limits, rations, and cooldowns are permanently bound to the **NFT Token ID**, never resetting upon wallet transfers.

---

## 2. Smart Contract Topology & Security Architecture

The protocol is divided into specialized contracts to strictly respect Ethereum's 24,576-byte bytecode cap (EIP-170), isolate economic risk, and allow presentation upgrades while keeping economic invariants immutable:

```mermaid
graph TD
    A["HoodQuest.sol (ERC-721 + Enumerable + EIP-4906)<br>Identity, Age, Stamina Counters, Armory Escrow"] 
    B["HoodQuestTreasures.sol (ERC-1155)<br>Royal Gold (ID 1), Gear, Blacksmith, Rebate Reserve"]
    C["HoodQuestCompanions.sol (ERC-721 + Enumerable)<br>10,000 Pets, Foraging, Bond Ranks"]
    D["HoodQuestRaids.sol (Combat & Action Engine)<br>Heists, Monthly Raids, Tax Train, Jubilees"]
    E["HoodQuestBazaar.sol (Native Camp Bazaar)<br>On-Chain Gold Trading with Loadout Freeze"]
    R["HoodQuestRenderer.sol (Replaceable Engine)<br>Procedural Vector Art & Metadata Strings"]

    A <--> B
    A <--> C
    A <--> D
    B <--> D
    C <--> D
    A <--> E
    B <--> E
    A -.->|staticcall (try/catch)| R
```

### Contract Responsibilities:

- **`HoodQuest.sol` (ERC-721 + `ERC721Enumerable` + EIP-4906 Core):**
  - Symbol: **`HQ`** | Maximum Supply: **`MAX_HOOD_SUPPLY = 10,000`** (Immutable constant).
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
  - **Mint Economics & Delayed Hero Seed Finalization:**
    - Testnet: `MINT_PRICE_WEI = 0` (free test mint); Mainnet: fixed immutable constant (e.g. `0.005 ETH`).
    - Proceeds withdrawable strictly to `PROCEEDS_RECIPIENT` (immutable multisig). No arbitrary fee parameters.
    - Transaction limit: Max 5 mints per transaction.
    - **Delayed Seed Assignment:** Minting does not assign instantaneous pseudo-random seeds. It schedules:
      ```solidity
      seedTargetBlock[tokenId] = ArbSys(0x64).arbBlockNumber() + 2;
      ```
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
              // Deterministic non-random fallback: assigns standard genesis trait set
              // Eliminates any rarity advantage from deliberately letting reveal expire
              heroSeed[tokenId] = keccak256(abi.encode("STANDARD_GENESIS", tokenId, GENESIS_TIME));
          }
          emit HeroSeedFinalized(tokenId, heroSeed[tokenId]);
      }
      ```
      Before seed finalization, the renderer displays an "Unrevealed Camp Outlaw" camp scene.
      **Economic Gameplay Requirement:** All heists, Castle maneuvers, and Boss attacks strictly require `heroSeed[hoodId] != bytes32(0)`.
  - **Stamina & Temporal State Authority:** The core permanently owns and tracks:
    - `baseHeistsUsed[tokenId]` (max 5/day)
    - `bonusHeistsUsed[tokenId]` (max 5/day via Elixir)
    - `lastHeistDay[tokenId]`
    - `lastCareDay[tokenId]`
    - `lastElixirDay[tokenId]`
    - `pendingNormalHeist[tokenId]` (boolean: strictly at most 1 pending heist batch per Hood)
    - `pendingGameplayCount[tokenId]` (unified counter for heists, castle maneuvers, and pending RNG)
    - `effectiveBiologicalAge[tokenId]`
    - Derived UTC day helper:
      ```solidity
      function currentUtcDay() public view returns (uint32) {
          return uint32(block.timestamp / 1 days);
      }
      ```
  - **O(1) Delegate Wiping via Delegation Epochs:**
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
    On every Hood transfer (`_update` when `from != to`), `delegateEpoch[hoodId]++` executes, invalidating all previously authorized delegates in $O(1)$.
  - **Delegate Permission Scope & Item Spending:**
    - Authorized delegates may call: `dailyCare`, `feed`, companion `soloForage`, `requestHeistBatch`, `resolveHeist`, `claimHeistRewards` (strictly to `ownerOf(hoodId)`), and `enterCastleHeist`.
    - **Inventory Rule:** When delegates call `feed(hoodId)` or `useElixir(hoodId)`, items are burned **strictly from `msg.sender` (the delegate's own wallet)**. Delegates can never spend or burn inventory owned by the Hood owner.
    - Delegates are **strictly forbidden** from: listing on Bazaar, transferring tokens, equipping items, bonding pets, initiating/finalizing unequips or debonds, and withdrawing assets.
  - **Presentation Upgradeability & Try/Catch Protected Fallback:**
    - 48-hour Timelock may replace `renderer` via `setRenderer(address newRenderer)`.
    - Verification guard: `require(newRenderer.code.length > 0, "Invalid renderer code")`.
    - Wrapped in `try/catch` with gas cap to strictly prevent malformed ABI returns from reverting:
      ```solidity
      function tokenURI(uint256 tokenId) public view override returns (string memory) {
          _requireOwned(tokenId);
          if (address(renderer) != address(0)) {
              try IRenderer(renderer).tokenURI{gas: 2_000_000}(tokenId) returns (string memory uri) {
                  if (bytes(uri).length > 0) return uri;
              } catch {}
          }
          return _fallbackTokenURI(tokenId);
      }
      ```

- **`HoodQuestTreasures.sol` (ERC-1155 Treasury & Accounting Authority):**
  - **Item Classification:**
    - `ID 1` = `CORE_CURRENCY` (Royal Gold Sovereign)
    - `IDs 2–9, 13–17` = `CORE_ONLY` (Genesis equipment, cloaks, bows, arrows, cornucopias, materials)
    - `IDs 10–12, 18–20` = `RESERVED_UNMINTABLE` (Reserved for future timelocked additions)
    - `IDs 21+` = `EXPANSION_REGISTRY` (timelocked registration)
  - **Single Accounting Authority:** Tracks `lifetimeMinted[id]`, `reservedUnclaimed[id]`, `circulatingSupply[id]`, `cumulativeGoldMinted`, `cumulativeGoldBurned`, and `rebateReserve`.
  - **Scarce Reward Reservation System:**
    ```solidity
    function reserveScarceItem(uint256 itemId) external onlyRaidEngine returns (bool) {
        uint256 cap = itemLifetimeCap[itemId];
        if (cap == 0) return true; // Uncapped
        if (lifetimeMinted[itemId] + reservedUnclaimed[itemId] < cap) {
            reservedUnclaimed[itemId]++;
            return true;
        }
        return false;
    }
    ```
  - **The Blacksmith Crafting State Machine:**
    Detailed in Section 5. Checks supply availability before burning, burns Gold through `_burnGold()`, burns Yew/Iron, and mints directly to crafter.
  - **Enforceable Soulbound Proof-of-Play (Yew #16 & Iron #17):**
    Checked strictly **before** state modification:
    ```solidity
    function _update(address from, address to, uint256[] memory ids, uint256[] memory values) internal override {
        for (uint256 i = 0; i < ids.length; i++) {
            if (ids[i] == YEW || ids[i] == IRON) {
                require(from == address(0) || to == address(0), "Soulbound material cannot be transferred");
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
        // Remaining 75% is permanently destroyed from circulating supply
    }
    ```

- **`HoodQuestCompanions.sol` (ERC-721 + `ERC721Enumerable`):**
  - Maximum Supply: **`MAX_COMPANION_SUPPLY = 10,000`** (4,000 Camp Hounds, 3,000 Hunting Falcons, 3,000 Barn Owls).
  - Implements `ERC721Enumerable` for instant on-chain discovery.
  - **Genesis Adoption Guard (1 Genesis Adoption per Hood Lifetime):**
    ```solidity
    mapping(uint256 => bool) public genesisAdoptionUsed;
    uint256 public nextHoundId = 1;     // 1..4000
    uint256 public nextFalconId = 4001; // 4001..7000
    uint256 public nextOwlId = 7001;    // 7001..10000

    function adoptGenesisPet(uint256 hoodId, uint8 species) external returns (uint256 petId) {
        require(hoodContract.ownerOf(hoodId) == msg.sender, "Not Hood owner");
        require(!genesisAdoptionUsed[hoodId], "Genesis pet already adopted for this Hood");
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
  - Executes daily batch heists, Monthly Castle Vault Infiltrations, Tax Train World Bosses, and 5-Year Jubilees using the unified `ActionRequest` engine.
  - Resolves mixed stamina batches, sequential fatigue, and scarce-reward reservations.

- **`HoodQuestBazaar.sol` (Native Camp Bazaar):**
  - Complete marketplace state machine with entitlement escrow, loadout hash verification, and paginated discovery.
  - Detailed in Section 4.

---

## 3. The Calibrated 25-Year Economic Engine & Heist State Machine

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

Furthermore, players can request up to 5 heists in a single transaction via `requestHeistBatch`. The core returns `(uint8 baseCount, uint8 bonusCount)`, enabling exact roll-by-roll classification:

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
    
    // Core consumes stamina and returns exact breakdown
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
        heroSeed: seed,
        snapshot: snap
    });
    
    hoodContract.setPendingNormalHeist(hoodId, true);
    hoodContract.incrementPendingGameplay(hoodId, count);
    emit HeistBatchRequested(requestId, hoodId, count, target);
}

function resolveHeist(uint256 requestId) external nonReentrant {
    HeistRequest memory req = heistRequests[requestId];
    require(req.targetBlock > 0, "Non-existent request");
    
    uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
    require(currentBlock > req.targetBlock, "Target block not reached");
    
    // Checks-Effects: Clear request and decrement pending counter BEFORE reward calculation
    delete heistRequests[requestId];
    hoodContract.setPendingNormalHeist(req.hoodId, false);
    hoodContract.decrementPendingGameplay(req.hoodId, req.count);
    
    RewardBundle memory bundle;
    bool fatigueActive = req.snapshot.initialFatigue;
    
    // Sync monthly active Hood if this batch contained at least one base heist
    if (req.baseCount > 0) {
        _syncMonthlyActiveHood(req.hoodId);
    }
    
    if (currentBlock <= req.targetBlock + 256) {
        bytes32 arbHash = ArbSys(address(0x64)).arbBlockHash(req.targetBlock);
        for (uint8 i = 0; i < req.count; i++) {
            bytes32 rollEntropy = keccak256(abi.encode(
                arbHash,
                requestId,
                req.hoodId,
                req.heroSeed,
                i,
                block.chainid
            ));
            
            bool isBonusRoll = (i >= req.baseCount);
            
            // Execute sequential roll with local fatigue propagation
            fatigueActive = _resolveSequentialRoll(
                req.hoodId,
                req.snapshot,
                rollEntropy,
                isBonusRoll,
                fatigueActive,
                bundle
            );
        }
        emit HeistBatchResolved(requestId, req.hoodId, req.count);
    } else {
        // Deterministic fallback: 1 Gold per heist, 0 rare rolls
        bundle.gold = req.count * 1;
        emit HeistFallbackResolved(requestId, req.hoodId, req.count);
    }
    
    // Write remaining fatigue state back to Hood core
    hoodContract.setFatigue(req.hoodId, fatigueActive);
    
    // Store rewards into escrow record (Reward Entitlement Escrow)
    _accrueRewardBundle(req.hoodId, bundle);
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
    treasuresContract.mintRewardBundle(recipient, bundle);
    emit HeistRewardsClaimed(hoodId, recipient);
}
```

### 3. Explicit Stamina & Elixir Priority Algorithm:
- **Daily Reset at 00:00 UTC:** When `currentUtcDay() > lastHeistDay[tokenId]`:
  `baseHeistsUsed = 0; bonusHeistsUsed = 0; lastHeistDay = currentUtcDay();`
- **Base Stamina:** Exactly 5 attempts per UTC day.
- **`useElixir(hoodId)`:**
  - Permitted caller: Hood owner or authorized game delegate.
  - Inventory requirement: Burns 1 Greenwood Elixir strictly from `msg.sender` (delegate cannot spend owner's inventory).
  - Requires Hood is awake (`!isSlumbering(hoodId)`).
  - Requires `lastElixirDay[hoodId] < currentUtcDay()` (strictly once per UTC day).
  - Sets `lastElixirDay[hoodId] = currentUtcDay()`. Unlocks 5 bonus heists (`bonusHeistsAvailable = 5`).
- **Consumption Priority in `consumeStaminaBatch(hoodId, count)`:**
  ```solidity
  uint8 baseRemaining = 5 - baseHeistsUsed[hoodId];
  if (count <= baseRemaining) {
      baseHeistsUsed[hoodId] += count;
      return (count, 0);
  } else {
      uint8 fromBase = baseRemaining;
      uint8 fromBonus = count - fromBase;
      require(lastElixirDay[hoodId] == currentUtcDay(), "Bonus stamina not unlocked");
      require(bonusHeistsUsed[hoodId] + fromBonus <= 5, "Exceeds daily bonus stamina");
      baseHeistsUsed[hoodId] = 5;
      bonusHeistsUsed[hoodId] += fromBonus;
      return (fromBase, fromBonus);
  }
  ```
- **Bonus Session Drop Rule:** During bonus rolls (`isBonusRoll == true`), the Greenwood Elixir drop probability is strictly **0%**, completely eliminating recursive Elixir farming loops.

### 4. Sequential Fatigue & Single Pending Batch Invariant:
- **Single Pending Batch Invariant:** At most **one unresolved normal-heist batch** may exist for any Hood at a time (`pendingNormalHeist[hoodId] == true`). This strictly prevents two pending batches from snapshotting the same fatigue state.
- **Sequential Fatigue Mechanics:**
  1. Roll 0 applies `fatigueActive` from `snapshot.initialFatigue` (which reduces rare drop probability by 25%).
  2. Roll 0 consumes the initial fatigue (`fatigueActive = false`).
  3. If Roll 0 suffers mitigated damage $> 20$, it sets `fatigueActive = true` for Roll 1.
  4. Each subsequent roll $i$ evaluates `fatigueActive`, consumes it, and conditionally sets `fatigueActive = true` for roll $i+1$.
  5. The final fatigue state after roll $count - 1$ is written back to `HoodQuest.sol`.

### 5. Starvation & Bonus Gold Fixed-Point Pipeline:
"Base roll of 1–3 Gold before economic modifiers". Starvation and Gold bonuses are processed through an integrated fixed-point carry pipeline:
```solidity
// Step 1: Base roll of 1-3 Gold
uint256 baseRoll = 1 + (uint256(rollEntropy) % 3);

// Step 2: Starvation / economic modifier with carry (5,000 bps starving / 10,000 bps fed)
uint256 econScaled = baseRoll * snapshot.economicRewardBps + economicGoldCarryBps[hoodId];
uint256 postEconGold = econScaled / 10_000;
economicGoldCarryBps[hoodId] = uint16(econScaled % 10_000);

// Step 3: Equipment & Devotion Gold bonus with carry
uint256 bonusScaled = postEconGold * snapshot.goldBonusBps + goldBonusCarry[hoodId];
uint256 bonusGold = bonusScaled / 10_000;
goldBonusCarry[hoodId] = uint16(bonusScaled % 10_000);

uint256 finalGoldReward = postEconGold + bonusGold;
bundle.gold += finalGoldReward;
```

### 6. Recalibrated Rare-Item Drop Rates (36.5M Max Heists/Yr):
Base drop rates are calibrated so that even with 10 heists/day and the maximum $2\times$ combat power multiplier, annual emissions match historical targets:
- 🌟 **Gilded Recurve Bow (#3):** Base rate = **`0.0000125%`** (max $2\times = 0.000025\% \approx 9$ direct drops/year at full population; remaining ~772 entered strictly via forging).
- ⚔️ **Finished Common-Weapon Steals:** Base rate = **`0.00025%`** (max $2\times = 0.0005\%$ across Longbows, Quarterstaffs, Daggers).
- 🍺 **Nottingham Mead Cask (#2):** Base rate = **`0.00125%`** (max $2\times = 0.0025\%$).
- 🍞 **Forest Feast Basket (#7):** Base rate = **`0.5%`** (craft cost: 14 Gold; covers only 17.5% of weekly food upkeep).
- 🧪 **Greenwood Elixir (#5):** Base rate = **`0.8%`** (craft cost: 25 Gold; max 1 used/day; 0% recursive drop during bonus rolls).
- 👑 **The Golden Arrow (#4):** Base rate = **`0%`** on normal heists (Reserved exclusively for Annual Solstice Heists and 5-Year Jubilees).
- **Scarce Reservation Guard:** If a rare item roll succeeds, `reserveScarceItem(itemId)` is called. If supply is exhausted, `emit CappedDropSkipped(tokenId, itemId)` is emitted with zero consolation Gold.

### 7. Unified Global `rebateReserve`:
All event budgets (Monthly Raids, Solstice Heists, Tax Train World Bosses, Jubilees) draw strictly from `rebateReserve`:
$$\text{eventBudget} = \min(\text{EVENT\_CAP}, \text{rebateReserve}); \quad \text{rebateReserve} -= \text{eventBudget};$$
**Global Invariant:** Total event reminting across the lifetime of HoodQuest can **never exceed 25% of Gold previously burned**.

---

## 4. The Armory Escrow Vault & Marketplace Shield

### 1. Loadout Guarantees: Native Bazaar vs. External OpenSea:
- **Native HoodQuest Bazaar (Cryptographically Guaranteed):**
  - A Hood cannot be listed unless `canList(hoodId)` returns true.
  - Escrows the Hood, freezes gameplay, and locks the typed loadout hash:
    ```solidity
    loadoutHash = keccak256(abi.encode(
        weaponId,
        armorId,
        ammoId,
        utilityId,
        sustenanceRelicId,
        decorId,
        petId,
        loadoutVersion
    ));
    ```
  - At purchase settlement, `loadoutHash` is re-evaluated; if mismatched, transaction reverts.
- **External Marketplaces (OpenSea / Seaport):**
  - Seaport off-chain signatures commit to `(contract, tokenId, price)`, not internal loadout state.
  - Formal protocol promise: **"Any equipment bound to the Hood at the exact instant of transfer follows the Hood; any pending unequip is automatically wiped and cancelled upon transfer."**
  - Metadata exports `loadout_version` so third-party frontends can detect changes before purchase.

### 2. The Bazaar Pre-Sale State Gate (`canList`):
```solidity
function canList(uint256 hoodId) public view returns (bool allowed, uint256 reasonFlags) {
    if (pendingGameplayCount[hoodId] > 0) reasonFlags |= 1;
    if (pendingUnequipCount[hoodId] > 0) reasonFlags |= 2;
    if (pendingDebondMaturesAt[hoodId] > 0) reasonFlags |= 4;
    if (hasActiveSolsticeCommitment[hoodId]) reasonFlags |= 8;
    if (hasPendingEventParticipation(hoodId)) reasonFlags |= 16;
    if (_hasUnclaimedHeistRewards(hoodId)) reasonFlags |= 32;
    allowed = (reasonFlags == 0);
}
```

### 3. Equipment & Pet Escrow State Machines:
- **7 Canonical Equipment Slots:**
  `0: Weapon`, `1: Armor`, `2: Ammo`, `3: Utility`, `4: SustenanceRelic`, `5: Decor`, `6: Companion`.
- **Per-Slot Unequip Timers:**
  ```solidity
  struct UnequipRequest {
      uint64 maturesAt;
      uint32 itemId;
  }
  mapping(uint256 => mapping(uint8 => UnequipRequest)) public pendingUnequip;
  mapping(uint256 => uint8) public pendingUnequipCount;
  ```
  - `initiateUnequip(hoodId, slot)`: Requires `equippedSlot[hoodId][slot] != 0` and no existing unequip request on `slot`.
    Sets `pendingUnequip[hoodId][slot] = UnequipRequest(uint64(block.timestamp + 24 hours), itemId)`.
    Increments `pendingUnequipCount[hoodId]++`.
  - `finalizeUnequip(hoodId, slot)`: Requires `block.timestamp >= req.maturesAt` and `equippedSlot[hoodId][slot] == req.itemId`.
    Clears request and internal binding **before** safeTransfer to `ownerOf(hoodId)` with `nonReentrant`.
    Increments `loadoutVersion[hoodId]++` and emits `MetadataUpdate(hoodId)`.
  - **Transfer Hook:** On NFT transfer, loops $0..6$ to delete all `pendingUnequip[hoodId][slot]` and resets `pendingUnequipCount[hoodId] = 0`.
- **`loadoutVersion` Mutation Rules:**
  Increments by 1 on every:
  1. `equipItem`
  2. `finalizeUnequip`
  3. `bondPet`
  4. `finalizeDebond`
  5. Cornucopia / Decor bind or unbind
  Emits `MetadataUpdate(hoodId)` (EIP-4906) on every increment. Does **not** increment merely for initiating an unequip/debond notice.

### 4. Native Camp Bazaar State Machine:
```solidity
struct Listing {
    address seller;
    uint256 price;
    bytes32 loadoutHash;
}

mapping(uint256 => Listing) public listings;
mapping(address => uint256) public bazaarProceedsEscrow;
uint256[] public activeListingTokenIds;
mapping(uint256 => uint256) public activeListingIndex;

function listHero(uint256 hoodId, uint256 price) external nonReentrant {
    require(price >= 40, "Minimum price is 40 Gold");
    (bool allowed, ) = canList(hoodId);
    require(allowed, "Hood not listable");
    require(hoodContract.ownerOf(hoodId) == msg.sender, "Not owner");
    
    bytes32 hash = hoodContract.getLoadoutHash(hoodId);
    listings[hoodId] = Listing(msg.sender, price, hash);
    
    activeListingIndex[hoodId] = activeListingTokenIds.length;
    activeListingTokenIds.push(hoodId);
    
    // Transfer Hood into Bazaar escrow
    hoodContract.transferFrom(msg.sender, address(this), hoodId);
    emit HeroListed(hoodId, msg.sender, price, hash);
}

function cancelListing(uint256 hoodId) external nonReentrant {
    Listing memory l = listings[hoodId];
    require(l.seller == msg.sender, "Not seller");
    
    _removeActiveListing(hoodId);
    delete listings[hoodId];
    
    hoodContract.transferFrom(address(this), msg.sender, hoodId);
    emit ListingCancelled(hoodId);
}

function buyListing(uint256 hoodId) external nonReentrant {
    Listing memory l = listings[hoodId];
    require(l.seller != address(0), "Not listed");
    require(hoodContract.getLoadoutHash(hoodId) == l.loadoutHash, "Loadout mutated");
    
    uint256 fee = l.price / 40; // Exact 2.5% integer floor
    uint256 sellerProceeds = l.price - fee;
    
    // Take payment from buyer
    treasuresContract.burnBazaarGold(msg.sender, l.price, fee);
    
    // Credit seller proceeds to entitlement escrow (safe for all receiver contracts)
    bazaarProceedsEscrow[l.seller] += sellerProceeds;
    
    _removeActiveListing(hoodId);
    delete listings[hoodId];
    
    hoodContract.transferFrom(address(this), msg.sender, hoodId);
    emit HeroPurchased(hoodId, msg.sender, l.seller, l.price);
}

function withdrawBazaarProceeds(address recipient) external nonReentrant {
    require(recipient != address(0), "Invalid recipient");
    uint256 amount = bazaarProceedsEscrow[msg.sender];
    require(amount > 0, "No proceeds");
    bazaarProceedsEscrow[msg.sender] = 0;
    treasuresContract.mintGold(recipient, amount);
    emit ProceedsWithdrawn(msg.sender, recipient, amount);
}

function getActiveListings(uint256 cursor, uint256 limit) external view returns (uint256[] memory tokenIds, uint256 nextCursor) {
    uint256 total = activeListingTokenIds.length;
    if (cursor >= total) return (new uint256[](0), 0);
    uint256 count = total - cursor > limit ? limit : total - cursor;
    tokenIds = new uint256[](count);
    for (uint256 i = 0; i < count; i++) {
        tokenIds[i] = activeListingTokenIds[cursor + i];
    }
    nextCursor = cursor + count < total ? cursor + count : 0;
}
```

---

## 5. Anti-Power-Creep Weapon, Combat Matrix & Blacksmith

### Statutory Stat Invariants:
1. `MAX_EFFECTIVE_ATK = 45` (Gilded Bow +20 + Golden Arrow +25 apex).
2. `MAX_EFFECTIVE_DEF = 30` (Locksley Cloak +20 + Camp Hound Rank 5 +10).
3. `MAX_EFFECTIVE_STEALTH = 30` (Twin Daggers +15 + Locksley Cloak +10 + Barn Owl Rank 5 +5).
4. `MAX_EFFECTIVE_MORALE = 15` (Silver Rallying Horn +10 + Minstrel Archetype +5).
5. `BASE_COMBAT_POWER = 50` (Baseline for ungeared Hoods).
6. `MAX_GOLD_MULTIPLIER = 40%` (Gilded Bow +20% + Owl Rank 5 +10% + Devotion +10%).
7. `MAX_CRIT_CHANCE = 25%` (Falcon Rank 5 +8% + archetype buffs clamp at 2,500 bps).

### Complete Canonical Arsenal & Blacksmith Recipes:

| ID | Item Name | Slot | Supply Semantics | Hard Cap | Blacksmith Craft Recipe | Primary Mechanics & Ceilings |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Royal Gold Sovereign** | Currency | `CORE_CURRENCY` | Dynamic | Base Drop | Universal currency (25% rebate / 75% burn) |
| **2** | **Nottingham Mead Cask** | `Decor` | `maxCirculating` | **5,000** | 5 🪙 | Campfire banter in SVG |
| **3** | **Gilded Recurve Bow** | `Weapon` | `splitCap` | **1,000** (750 Forge / 250 Drop) | 60 🪙 + 5 Yew + 5 Iron | **+20 ATK & +20% Gold Multiplier** |
| **4** | **The Golden Arrow** | `Ammo` | `maxLifetimeMinted` | **25** | Event Prize Only | **+25 ATK** (Requires Bow; non-consumable) |
| **5** | **Greenwood Elixir** | Consumable | `maxCirculating` | **2,500** | 25 🪙 | **+5 Heists** (Max 1/day; 0% recursive drop) |
| **6** | **Locksley Velvet Cloak** | `Armor` | `maxLifetimeMinted` | **750** | 30 🪙 + 2 Yew + 2 Iron | **+20 DEF & +10 STEALTH** |
| **7** | **Forest Feast Basket** | Sustenance | `uncappedSupply` | Consumable | 14 🪙 | **7-Day Rations:** Max 56d stored; stops starvation |
| **8** | **Silver Rallying Horn** | `Utility` | `maxLifetimeMinted` | **500** | 35 🪙 + 3 Yew + 3 Iron | **+10 MORALE** (Castle Infiltration Aura) |
| **9** | **Friar's Cornucopia** | `SustenanceRelic` | `maxLifetimeMinted`| **25** | 5-Yr Jubilee Only | **Permanent Fed State** (7-day min bind; feeds 1 Hood) |
| **13**| **Yew Forest Longbow** | `Weapon` | `maxLifetimeMinted` | **10,000** | 10 🪙 + 2 Yew | **+10 ATK** (Common Bow) |
| **14**| **Oak Quarterstaff** | `Weapon` | `maxLifetimeMinted` | **2,500** | 20 🪙 + 3 Yew + 1 Iron | **+15 DEF / STUN** (Brawler Weapon) |
| **15**| **Poacher's Twin Daggers**| `Weapon` | `maxLifetimeMinted` | **1,500** | 25 🪙 + 1 Yew + 3 Iron | **+15 STEALTH** (Infiltration Weapon) |
| **16**| **Sherwood Yew (Timber)** | Material | `uncappedSoulbound`| Soulbound | Quest Drop (25%) | **Proof of Play:** Soulbound timber |
| **17**| **Nottingham Iron (Steel)**| Material | `uncappedSoulbound`| Soulbound | Quest Drop (20%) | **Proof of Play:** Soulbound steel |

*IDs 10–12 and 18–20 are explicitly `RESERVED_UNMINTABLE` in V1.*

### The Blacksmith Crafting Execution State Machine:
```solidity
function craft(uint256 itemId, uint256 quantity) external nonReentrant {
    require(quantity > 0, "Quantity must be > 0");
    require(!hoodContract.economicActionsPaused(), "Economic actions paused");
    
    CraftRecipe memory r = craftRecipes[itemId];
    require(r.isValid, "Item not craftable");
    
    // Check split caps or lifetime caps BEFORE burning
    if (itemId == GILDED_BOW) {
        require(forgedGildedBows + quantity <= 750, "Forge cap for Gilded Bows reached");
        forgedGildedBows += quantity;
    } else if (r.isCapped) {
        require(lifetimeMinted[itemId] + reservedUnclaimed[itemId] + quantity <= r.cap, "Cap reached");
    }
    
    // Burn Gold through rebate reserve
    _burnGold(msg.sender, r.goldCost * quantity);
    
    // Burn materials
    if (r.yewCost > 0) _burn(msg.sender, YEW, r.yewCost * quantity);
    if (r.ironCost > 0) _burn(msg.sender, IRON, r.ironCost * quantity);
    
    lifetimeMinted[itemId] += quantity;
    _mint(msg.sender, itemId, quantity, "");
    emit ItemCrafted(msg.sender, itemId, quantity);
}
```

### Golden Arrow & Cornucopia Invariants:
1. **Bow Dependency for Golden Arrow:**
   ```solidity
   require(
       equippedSlot[hoodId][SLOT_WEAPON] == GILDED_BOW ||
       equippedSlot[hoodId][SLOT_WEAPON] == YEW_LONGBOW,
       "Golden Arrow requires equipped bow"
   );
   ```
   A bow cannot be unequipped while the Golden Arrow remains in `SLOT_AMMO`.
2. **Friar's Cornucopia Economic Exclusivity & Slumber Rule:**
   - Feeds exactly one currently bound Hood (`isFed(hoodId) == true` unconditionally).
   - **Campfire Care Invariant:** Cornucopia prevents starvation penalties, but does **not** replace daily care for slumber purposes. If `dailyCare(hoodId)` is not performed within 3 days, the Hood slumbers regardless of the Cornucopia.
   - 7-day minimum bind period before unequip can be initiated:
     ```solidity
     require(block.timestamp >= cornucopiaBoundTimestamp[hoodId] + 7 days, "Cornucopia 7-day bind lock active");
     ```

---

## 6. Mother Meg's Rescue Post & Companion Sidecars

Companions are managed by `HoodQuestCompanions.sol`:
- **Supply Cap:** **10,000 Total Genesis Companions** (4,000 Hounds, 3,000 Falcons, 3,000 Owls).
- **Genesis Adoption Limit:** Each Hood may adopt at most 1 Genesis companion in its lifetime (`genesisAdoptionUsed[hoodId] = true`), guaranteeing 1:1 parity with the 10,000 Hood population.
- **Pet Biological Age Derived from Host Hood Biological Clock:**
  ```solidity
  function effectivePetAge(uint256 petId) public view returns (uint256) {
      uint256 hoodId = petBoundToHood[petId];
      if (hoodId == 0) return accumulatedPetActiveSeconds[petId];
      uint256 hoodCurrentAge = hoodContract.effectiveBiologicalAge(hoodId);
      return accumulatedPetActiveSeconds[petId] + (hoodCurrentAge - hoodEffectiveAgeAtBond[petId]);
  }
  ```
  Because Hood biological age already pauses during slumber, pet biological age automatically freezes without cross-contract keepers or callbacks!
- **Pet Age Stage (Cosmetic, Time-Based):** Juvenile (Day 0) → Young (Yr 1) → Adult (Yr 5) → Elder (Yr 10) → Ancient Legend (Yr 25).
- **Pet Bond Rank (Gameplay, XP-Based):**
  - Earned strictly via daily solo foraging (+10 Pet XP/day):
    - **Rank 1:** `0 XP`
    - **Rank 2:** `300 XP` (~30 forage days)
    - **Rank 3:** `900 XP` (~90 forage days)
    - **Rank 4:** `1,800 XP` (~180 forage days)
    - **Rank 5:** `3,650 XP` (~365 forage days)
  - Perks by Rank:
    - 🐕 **Camp Hound:** +2 DEF (Rank 1) → +4 → +6 → +8 → **+10 DEF (Rank 5)**.
    - 🦅 **Hunting Falcon:** +2% Crit (Rank 1) → +3% → +5% → +6% → **+8% Crit (Rank 5)**.
    - 🦉 **Barn Owl:** +3% Gold / +1 Stealth (Rank 1) → +5%/+2 → +7%/+3 → +8%/+4 → **+10% Gold / +5 Stealth (Rank 5)**.
- **Deterministic Daily Solo Foraging:**
  - 1 forage / pet / UTC day (`lastForageDay[petId] < currentUtcDay()`).
  - Deterministic non-rerollable on-chain entropy:
    ```solidity
    bytes32 forageEntropy = keccak256(abi.encode(
        petSeed[petId],
        petId,
        currentUtcDay(),
        address(this),
        block.chainid
    ));
    ```
  - Awards +10 Pet XP (100%).
  - Sherwood Yew (12%): `uint16(uint256(forageEntropy) % 10_000) < 1200`.
  - Nottingham Iron (8%): `uint16((uint256(forageEntropy) >> 16) % 10_000) < 800`.
  - Strictly drops 0 Gold, 0 Elixirs, 0 Baskets, and 0 Tradeable gear.

---

## 7. The Upkeep, Slumber & Calibrated Devotion System

### 1. Daily Care Function & Slumber Settlement:
```solidity
function dailyCare(uint256 hoodId) external {
    require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(lastCareDay[hoodId] < currentUtcDay(), "Already cared today");
    _settleSlumber(hoodId);
    lastCareDay[hoodId] = currentUtcDay();
    lastCareTimestamp[hoodId] = uint64(block.timestamp);
    emit DailyCarePerformed(hoodId, currentUtcDay());
}
```

### 2. Starvation & 56-Day / 8-Basket Feeding State Machine:
- **Modifier Matrix:**
  - `fed + awake`: `economicRewardBps = 10,000` (100% yields).
  - `starving + awake`: `economicRewardBps = 5,000` (50% penalty with carry).
  - `slumbering`: Heists unavailable (`revert HeroSlumbering`).
- **Feeding Function (Clean 56-Day Cap):**
  ```solidity
  function feed(uint256 hoodId) external {
      require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
      _settleSlumber(hoodId);
      // Burns basket strictly from msg.sender (delegates pay with their own inventory)
      treasuresContract.burnRationBasket(msg.sender, 1);
      
      uint256 currentRations = rationsUntil[hoodId];
      uint256 baseTime = currentRations > block.timestamp ? currentRations : block.timestamp;
      uint256 newRations = baseTime + 7 days;
      require(newRations <= block.timestamp + 56 days, "Max 8 baskets / 56 days prepayment");
      
      rationsUntil[hoodId] = uint64(newRations);
      emit HeroFed(hoodId, newRations);
  }
  ```

### 3. Derived Lazy Slumber State Machine:
- `careUntil = lastCareTimestamp[tokenId] + 3 days`
- `protectedUntil = max(careUntil, rationsUntil[tokenId])`
- `isSlumbering(tokenId) => block.timestamp > protectedUntil`
- Real-Time Effective Age Formula:
  $$\text{Effective Age} = (\text{isSlumbering}(tokenId) ? \text{protectedUntil} : \text{block.timestamp}) - \text{mintTimestamp}[tokenId] - \text{completedSlumberSeconds}[tokenId]$$
- Zero Slumber Farming: Slumbering heroes cannot initiate heists or raids.

### 4. Devotion Clocks Unified with Effective Biological Age:
$$\text{devotionSeconds} = \text{effectiveBiologicalAge}(\text{hoodId})$$
- **Month 1 (30 Days Awake):** +2% Gold bonus & firefly embers in SVG.
- **Month 3 (90 Days Awake):** +4% Gold bonus & `"Sherwood Tracker"` on-chain title (Wild Berry removed from V1).
- **Month 6 (180 Days Awake):** +6% Gold bonus & steaming kettle in SVG.
- **Year 1 (360 Days Awake):** **+10% Gold bonus (Permanent Hard Ceiling)** & `"Devoted Ranger"` on-chain title.

---

## 8. Gas-Free On-Chain Minigames & Artisan Vector Art Pipeline

```mermaid
flowchart LR
    subgraph View1 ["1. On-Chain Dynamic SVG (tokenURI 'image')"]
        A1["100% Procedural Vector Compiled by Solidity"]
        A2["• Anatomical Sloping Shoulders & Hand Anchors<br>• Paper-Doll Layered Generative Traits<br>• Aging & Silver Hair Milestones (Stage 4/5)<br>• Day 0 Juvenile Companions & Celestial Spirits"]
    end

    subgraph View2 ["2. Interactive Minigame (tokenURI 'animation_url')"]
        B1["100% On-Chain Data URI HTML/Canvas (Zero Servers)"]
        B2["• Weapon-Specific Ballistics & Collision Physics<br>• Non-Piercing Rebounds, Foam Smashes & Soundwaves<br>• Camp Backdrop Props & Toggle Simulation<br>• Cosmetic Petting (Purrs, Wiggles, Hearts)"]
    end
```

### 1. The Paper-Doll Generative Trait Pipeline:
- **Melanin & Skin Tone Palette:** 5 distinct procedural undertones (Fair Rose, Warm Peach, Olive Tan, Weathered Bronze, Deep Umber) paired with calibrated facial shading, cheek blush, and lip tones.
- **Anatomical Geometry & Hand Anchors:**
  - Natural sloping scapular curves and tapered necks replace rigid block models.
  - **Zero Floating Weapons:** All weapons pass directly through the character's hand geometry (`quadraticCurveTo`), with knuckles curled over the riser/grip.
- **Folklore Hair & Distinctive Headwear:**
  - *Friar Tuck:* Anatomically sculpted bald tonsure crown with dark chestnut horseshoe hair ring wrapping seamlessly around temples, ears, and nape; monastic cowl draped over shoulders.
  - *Robin Hood:* Lincoln Green bycocket with folded rear brim, red pheasant feather, and Van Dyke goatee.
  - *Little John:* Massive athletic frame, braided leather headband, and cascading wavy beard.
  - *Much the Miller:* Youthful tousled fringe, undyed miller's linen hood draped down back, and forager slingshot.
  - *Maid Marian & Mother Meg:* Multi-layer hair rendering (back locks cascade behind torso while front tresses drape gracefully over the gown collar with zero seam disconnect); filigree tiaras and floral alchemist circlets.
  - *Silver Hair Maturity:* Heroes reaching Stage 4 and Stage 5 (10 to 25+ Effective Years) develop silver-frosted hair and beards (`#a6adb5`).

### 2. Realistic Projectile & Impact Mechanics:
- **Piercing Projectiles (`arrow`, `stiletto`, `iron_bolt`, `duelist_blade`):** Stick securely point-first into the wooden straw target upon collision.
- **Blunt Rebound (`oak_cudgel`):** Bludgeons bounce off the target with wood splinter particles, falling to the ground.
- **Ale Foam & Target Dripping (`ale_mug`):** Smashes against the target, releasing frothy foam particles and leaving dripping ale trails (`beerDripTimer`).
- **Alchemical Detonation (`potion`):** Shatters into swirling mystic smoke clouds (`magic` particles).
- **Harmonic Sonic Waves (`harmonic_note`):** Radiates expanding concentric golden acoustic rings (`soundwaveTimer`).
- **Ricochet & Scatter (`acorn`, `coin_pouch`):** Acorns bounce with dull wooden thuds; coin pouches burst open to scatter golden sparks.

### 3. Day 0 Companion Immersion & Backdrop Props:
- Rescued companions appear immediately in camp as juvenile Pups, Chicks, and Owlets (scaled at 0.72x).
- Interactive backdrop props can be toggled: Target Range, Fireplace Hearth, Armory Weapon Rack, Mother Meg's Alchemy Bench, Gold Hoard Chest, Nottingham Mead Cask, Forest Feast Basket, and Timber Lodge Shelter.

---

## 9. The Sherwood Astronomical Calendar & World Events Engine

### 1. Sherwood Astronomical Calendar & Zero-Based / Human Conversion:
$$\text{Calendar Year} = 12 \text{ Months of 30 Days (Days 1–360)} + 5 \text{ Intercalary Solstice Days (Days 361–365)}$$

```solidity
uint256 elapsed = block.timestamp - GENESIS_TIME;
uint256 worldYearIndex  = elapsed / 365 days; // 0-based
uint256 worldYearNumber = worldYearIndex + 1; // 1-based (Human Years 1..25+)
uint256 dayOfYear = (elapsed % 365 days) / 1 days;

uint256 monthInYear = dayOfYear < 360 ? dayOfYear / 30 : 11; // Solstice days 360..364 belong to Month-12 epoch
uint256 monthEpoch = worldYearIndex * 12 + monthInYear;
```

```mermaid
flowchart TD
    subgraph MonthlyCycle ["1. Monthly Provincial Raids (Months 1–11)"]
        M1["Days 28–30 of Months 1–11 (Indices 27..29)"] --> M2["🏰 Monthly Castle Vault Infiltration<br>• 5 Infiltration Maneuvers per Hood<br>• Dynamic Breach Target: max(1,000, activeHoods x 60)<br>• Max Budget: 5,000 Gold (from Rebate Reserve)<br>• Monthly 'Master Infiltrator' Title & Silver Laurel"]
    end

    subgraph SolsticeClimax ["2. The Grand Royal Solstice Vault Heist (Month 12 / Solstice)"]
        A1["Days 359–365 (Indices 358..364)"] --> A2["👑 Grand Royal Solstice Vault Heist<br>• Spans final 2 days of Month 12 + 5 Solstice Days<br>• Sequential Player Secret Commitments + Delayed L2 Entropy<br>• Supreme Champion wins The Golden Arrow (Slots 0–19, 1/yr)"]
    end

    M2 -->|"Months 1 through 11"| M2
    M2 -->|"Month 12 Grand Solstice"| A2
```

### 2. O(1) Monthly Active Hood Tracking & Five Infiltration Sectors:
- **O(1) Per-Hood Active Month Storage:**
  ```solidity
  mapping(uint256 => uint32) public lastActiveMonth;
  mapping(uint32 => uint32) public monthlyActiveHoodCount;

  function _syncMonthlyActiveHood(uint256 hoodId) internal {
      if (lastActiveMonth[hoodId] != monthEpoch) {
          lastActiveMonth[hoodId] = monthEpoch;
          monthlyActiveHoodCount[monthEpoch]++;
      }
  }
  ```
  Dynamic community target: $\text{breachTarget} = \max(1,000, \text{monthlyActiveHoodCount}[monthEpoch - 1] \times 60)$.
- **Five Infiltration Sector Equations:**
  $$\begin{aligned}
  \text{Power}_{\text{Ramparts}} &= 50 + \text{effectiveATK} + (\text{effectiveCritBps} / 100) \\
  \text{Power}_{\text{Gatehouse}} &= 50 + \text{effectiveDEF} + (\text{effectiveATK} / 2) \\
  \text{Power}_{\text{Vault}} &= 50 + \text{effectiveSTEALTH} + (\text{effectiveATK} / 2) \\
  \text{Power}_{\text{Tavern}} &= 50 + (\text{effectiveDEF} / 2) + (\text{effectiveMORALE} \times 2) \\
  \text{Power}_{\text{Smokescreen}} &= 50 + \text{effectiveSTEALTH} + (\text{effectiveMORALE} \times 2)
  \end{aligned}$$

### 3. Solstice Championship Secret Commitment & Sequential Maneuvers:
- **Sequential Maneuver Enforcement:** A Hood must reveal or expire maneuver $N$ before committing maneuver $N+1$.
- `solsticeTargetBlock[hoodId] = ArbSys(0x64).arbBlockNumber() + 2`.
- Reveal window: `target < current && current <= target + 256`.
- Domain-separated reveal entropy:
  $$\text{Entropy} = \text{keccak256}(\text{abi.encodePacked}(\text{arbBlockHash}, \text{secret}, \text{hoodId}, \text{eventYear}, \text{maneuverIndex}))$$
- **Post-Year-20 Rule:**
  - Years 1–20: Champion wins The Golden Arrow (Slots 0–19) + Sovereign title.
  - Years 21+: Event continues forever; champion receives permanent crest + Gold bounty, but **no new Golden Arrow** (lifetime mint strictly capped at 25).

### 4. Boss Systems & Non-Overlapping Schedule:
- **The Sheriff's Iron Tax Train (Economy Threshold Boss):**
  - Triggers when `cumulativeGoldBurned >= nextBossThreshold` (threshold increments by 150,000 Gold).
  - 7-day battle; 14-day mandatory peace cooldown. Max budget: **25,000 Gold** (drawn from `rebateReserve`).
  - **Festival Suspension Rule:** During Jubilee (Days 351–357) and Solstice (Days 359–365), **no new Tax Train activates**. If the threshold is crossed, activation queues until the festival concludes.
- **The Sherwood Jubilee (Scheduled 5-Year Climax Boss):**
  - Triggers strictly when `worldYearNumber % 5 == 0 && worldYearNumber <= 25` on **Days 351–357**. Day 358 is an inter-festival buffer.
  - Max Gold Budget: **25,000 Gold** (from `rebateReserve`).
  - Bounded $O(5)$ leaderboard: Rank #1 receives that Jubilee's Golden Arrow (Slots 20–24); Top 5 receive the 5 Friar's Cornucopias (5 Cornucopias × 5 Jubilees = exactly 25 Cornucopias lifetime max).

### 5. Loop-Free Pro-Rata Event Payouts & Expiration:
```solidity
struct EventRecord {
    uint256 finalBudget;
    uint256 totalContribution;
    uint256 claimDeadline;
    uint256 claimedTotal;
    bool finalized;
}

mapping(uint256 => EventRecord) public eventRecords;
mapping(uint256 => mapping(uint256 => uint256)) public hoodContribution;
mapping(uint256 => mapping(uint256 => bool)) public eventClaimed;

function claimEventReward(uint256 eventId, uint256 hoodId) external nonReentrant {
    require(msg.sender == hoodContract.ownerOf(hoodId), "Not owner");
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Event not finalized");
    require(block.timestamp < e.claimDeadline, "Claim window expired");
    require(!eventClaimed[eventId][hoodId], "Already claimed");
    
    uint256 userContribution = hoodContribution[eventId][hoodId];
    require(userContribution > 0, "Zero contribution");
    
    eventClaimed[eventId][hoodId] = true;
    uint256 reward = (e.finalBudget * userContribution) / e.totalContribution;
    e.claimedTotal += reward;
    
    treasuresContract.mintGold(msg.sender, reward);
    emit EventRewardClaimed(eventId, hoodId, msg.sender, reward);
}

function refundUnclaimedEventBudget(uint256 eventId) external {
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp >= e.claimDeadline, "Claim window active");
    
    uint256 unclaimed = e.finalBudget - e.claimedTotal;
    e.claimedTotal = e.finalBudget; // Prevent double refunds
    
    treasuresContract.refundToRebateReserve(unclaimed);
    emit UnclaimedBudgetRefunded(eventId, unclaimed);
}
```

---

## 10. Bounded-Emission Governance & Expansion Blueprint

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

### 2. Authorization-Time Cap Check & Revocation Solvency:
- Daily emission ceiling across all active expansion modules:
  $$\text{allocatedAuthorizedDailyCap} \le 25,000 \text{ Gold/day}$$
- **Timelock Revocation & Re-Enabling State Machine:**
  ```solidity
  uint256 public allocatedAuthorizedDailyCap;
  mapping(address => uint256) public moduleDailyCap;
  mapping(address => bool) public isModuleAuthorized;

  function setModuleAuthorization(address module, bool authorized) external onlyTimelock {
      require(moduleDailyCap[module] > 0, "Unregistered module");
      if (authorized && !isModuleAuthorized[module]) {
          require(allocatedAuthorizedDailyCap + moduleDailyCap[module] <= 25_000, "Exceeds 25k daily cap");
          allocatedAuthorizedDailyCap += moduleDailyCap[module];
          isModuleAuthorized[module] = true;
      } else if (!authorized && isModuleAuthorized[module]) {
          allocatedAuthorizedDailyCap -= moduleDailyCap[module];
          isModuleAuthorized[module] = false;
      }
      emit ModuleAuthorizationChanged(module, authorized);
  }
  ```

### 3. Timelock Controller Role Graph:
- OpenZeppelin `TimelockController` architecture:
  - **Proposer:** Multi-signature governance council.
  - **Executor:** Permissionless execution by any address after 48-hour delay matures.
  - **Admin:** The Timelock is its own admin. Deployer has zero independent authority post-initialization.

---

## 11. Master Pre-Flight Audit & Verification Lifecycle Matrix

### Engineering Verification Lifecycle:
All audit items must be tracked across the formal verification lifecycle:
`Specified` $\rightarrow$ `Implemented` $\rightarrow$ `Unit Tested` $\rightarrow$ `Fuzz Tested` $\rightarrow$ `Invariant Tested` $\rightarrow$ `Testnet Verified` $\rightarrow$ `Independently Reviewed` $\rightarrow$ `Mainnet Ready`.

| Security Domain | Vulnerability / Threat | Proposed On-Chain Defense Mechanism | Engineering Status |
| :--- | :--- | :--- | :--- |
| **Mixed Stamina Batches** | Boolean cannot express mixed base/bonus attempts | **(baseCount, bonusCount) Breakdown:** Roll $i < baseCount$ is base; $i \ge baseCount$ is bonus (0% Elixir drop). | `[Specified]` |
| **Sequential Fatigue Propagation** | Parallel rolls all consuming the same fatigue flag | **Sequential Batch Loop:** Local `fatigueActive` propagated roll-by-roll; single pending batch invariant per Hood. | `[Specified]` |
| **Hero Seed Requirement & Reroll Exploit** | Fresh Hood playing unseeded; deliberately expiring reveal | **Mandatory Seed & Fixed Fallback:** Seed required for all economic play; expired reveal assigns standard genesis traits. | `[Specified]` |
| **Delegate Reward Theft** | Delegates claiming heist rewards to arbitrary addresses | **Owner-Only Claims:** Arbitrary recipient claim is owner-only; delegates may claim strictly to `ownerOf(hoodId)`. | `[Specified]` |
| **O(1) Delegate Wiping on Transfer** | Gas exhaustion attempting to clear nested mappings | **Delegation Epochs:** `delegateEpoch[hoodId]++` on transfer invalidates all delegates in $O(1)$. | `[Specified]` |
| **Blacksmith Crafting State Machine** | Crafting described in economy without state machine | **Executable craft():** Pre-burn cap checks, Gold burn via `_burnGold()`, material burn, and direct minting. | `[Specified]` |
| **Scarce-Reward Reservation** | Capped item claimed after supply exhausted by crafters | **Resolution Reservation:** `reserveScarceItem()` locks cap at resolution time; skips with `CappedDropSkipped` if full. | `[Specified]` |
| **Explicit Common Weapon Drops** | Generic `bows` field omitting common drop classes | **Explicit RewardBundle Fields:** Fixed fields for `gildedBows`, `yewLongbows`, `quarterstaffs`, `poacherDaggers`. | `[Specified]` |
| **Rare Scarcity Calibration** | 10 heists/day doubling historical drop emissions | **Halved Base Probabilities & Split Cap:** Gilded Bow base = 0.0000125%; 750 Forge Cap / 250 Direct Drop Cap. | `[Specified]` |
| **Starvation Gold Fixed-Point Carry** | Indivisible Gold truncated to zero on 1 Gold rolls | **Dual-Stage Carry Pipeline:** `economicGoldCarryBps` preserves 50% starvation yield over time. | `[Specified]` |
| **Per-Slot Unequip Timers** | Single unequip timer colliding across 7 slots | **pendingUnequip[hoodId][slot]:** Exact `(maturesAt, itemId)` recorded per slot; loops 0..6 on transfer to wipe. | `[Specified]` |
| **Explicit loadoutVersion Mutation** | Marketplaces unable to track loadout changes | **Strict Increment Rules:** Increments on equip, finalized unequip, bond, and finalized debond; emits EIP-4906. | `[Specified]` |
| **Bazaar State Machine & Discovery** | Missing marketplace lifecycle and listing arrays | **Entitlement Escrow & Arrays:** Complete list/cancel/buy state machine with `getActiveListings(cursor, limit)`. | `[Specified]` |
| **Loop-Free Event Reward Accounting** | Finalization looping through all participants | **Pro-Rata Pull Claims:** Claim computes share; permissionless `refundUnclaimedEventBudget()` refunds reserve. | `[Specified]` |
| **O(1) Per-Hood Active Month Storage** | Permanent per-month storage creating millions of slots | **lastActiveMonth Mapping:** Exactly one storage slot per Hood updated when `lastActiveMonth[hoodId] != monthEpoch`. | `[Specified]` |
| **World Year 0-Based / 1-Based Alignment** | Elapsed / 365d producing off-by-one Jubilee dates | **Explicit Derivation:** `worldYearIndex = elapsed / 365d`; `worldYearNumber = index + 1`; Jubilees on Years 5, 10, 15, 20, 25. | `[Specified]` |
| **Solstice Target Block & Sequential Maneuvers**| Maneuver target blocks unstated; concurrent actions | **Sequential Queue:** Explicit target block +2; window 256 blocks; maneuver $N+1$ requires reveal/expiry of $N$. | `[Specified]` |
| **Unified ActionRequest Engine** | Bespoke RNG systems for Castle, Tax Train, Jubilee | **Shared Action Engine:** Reusable delayed entropy engine with snapshotted stats and deterministic resolution. | `[Specified]` |
| **Pet Seed & Species Counters** | Pet seed unassigned; sequential counter crossing ranges | **Hood Seed Hashing & Separate Counters:** Hound (1..4k), Falcon (4001..7k), Owl (7001..10k) separate state counters. | `[Specified]` |
| **Cornucopia Campfire Care Invariant** | Cornucopia owner abandoning Hood for 25 years | **Care Still Required:** Cornucopia provides fed status but does not replace care; slumber occurs after 3 days without care. | `[Specified]` |
| **Try/Catch Renderer Protection** | Malformed ABI bytes reverting tokenURI | **try/catch Interface Staticcall:** 2M gas cap; cleanly catches reverts and malformed bytes, returning fallback. | `[Specified]` |
| **Expansion Daily Cap Solvency** | Revoking and re-enabling modules exceeding 25k cap | **allocatedAuthorizedDailyCap:** Decremented on disable, requires $\le 25,000$ on enable. | `[Specified]` |
| **Delegate Inventory Spending Rule** | Ambiguity over whose items are burned by delegates | **Caller Pays:** Delegates call `feed` and `useElixir` using strictly their own inventory (`msg.sender`). | `[Specified]` |
| **Clean 56-Day Rations Cap** | Awkward 60-day cap with 7-day baskets | **56-Day / 8-Basket Cap:** Exactly 8 baskets maximum prepayment (`now + 56 days`). | `[Specified]` |

---

## 12. Mainnet Acceptance Test & Invariant Specification

Before promoting this specification to Mainnet deployment, the smart contracts must satisfy these 18 formal mathematical invariants in Foundry unit and fuzz test suites:

### INV-1: Hood Token Supply & ID Invariant
$$\sum_{i=1}^{\infty} \mathbf{1}_{\{ \text{exists}(i) \}} \le 10,000 \quad \land \quad \forall i \in \text{HoodTokens}: 1 \le i \le 10,000$$

### INV-2: Mythic Grail Lifetime Mint Ceilings
$$\text{lifetimeMinted}[4] + \text{reservedUnclaimed}[4] \le 25 \quad \land \quad \text{lifetimeMinted}[9] + \text{reservedUnclaimed}[9] \le 25$$

### INV-3: Companion Genesis Parity & Adoption Limit
$$\forall h \in [1, 10000]: \text{genesisAdoptionCount}(h) \le 1 \quad \land \quad \text{totalCompanionsMinted} \le 10,000$$

### INV-4: Identity-Bound Temporal Tracking
$$\forall \text{transfer}(from, to, tokenId): \text{stamina}(tokenId)_{\text{post}} = \text{stamina}(tokenId)_{\text{pre}}$$

### INV-5: Starvation Economic Multiplier Clamp
$$\text{economicRewardBps}(h) = \begin{cases} 10,000 & \text{if } \text{isFed}(h) \land \neg\text{isSlumbering}(h) \\ 5,000 & \text{if } \neg\text{isFed}(h) \land \neg\text{isSlumbering}(h) \\ 0 & \text{if } \text{isSlumbering}(h) \end{cases}$$

### INV-6: Slumbering Action Prohibition
$$\forall h: \text{isSlumbering}(h) \implies \text{requestHeistBatch}(h, \cdot) \to \text{revert}(\text{HeroSlumbering})$$

### INV-7: Bounded Expansion Emission Ceiling
$$\text{allocatedAuthorizedDailyCap} \le 25,000 \text{ Gold/day}$$

### INV-8: Armory Vault Custody Integrity
$$\forall s \in \text{BoundSlots}(h): \text{withdraw}(h, s) \to \text{recipient} \equiv \text{ownerOf}(h)$$

### INV-9: Global Rebate Reserve Solvency
$$\sum \text{EventRewardsMinted} \le \text{cumulativeGoldBurned} \times 0.25$$

### INV-10: Delayed Entropy Terminal State Guarantee
$$\forall r \in \text{Requests}: \exists t < \infty \text{ s.t. } \text{state}(r) \in \{\text{Resolved}, \text{FallbackResolved}\}$$

### INV-11: Mixed Stamina Batch Roll Classification
$$\forall i < \text{baseCount}: \text{isBonus}(i) = \text{false}; \quad \forall i \ge \text{baseCount}: \text{isBonus}(i) = \text{true} \land \text{ElixirDropProb}(i) = 0$$

### INV-12: Single Pending Heist Batch Invariant
$$\forall h: \text{pendingNormalHeist}(h) \implies \text{requestHeistBatch}(h, \cdot) \to \text{revert}$$

### INV-13: Delegate Asset Non-Redirection & Inventory Spending
$$\forall \text{delegateCalls}: \text{claimHeistRewards} \to \text{recipient} \equiv \text{ownerOf}(h) \quad \land \quad \text{burn}(\text{Basket/Elixir}) \to \text{from} \equiv \text{msg.sender}$$

### INV-14: Scarce-Reward Reservation Solvency
$$\forall \text{itemId}: \text{lifetimeMinted}[\text{itemId}] + \text{reservedUnclaimed}[\text{itemId}] \le \text{cap}[\text{itemId}]$$

### INV-15: Bi-Directional Slot-Binding Integrity
$$\forall (h, s): \text{equippedSlot}[h][s] = \text{itemId} \iff \text{itemBoundTo}[s][\text{itemId}] = h$$

### INV-16: Per-Slot Unequip Request Isolation
$$\forall s_1 \ne s_2: \text{pendingUnequip}[h][s_1] \text{ independent of } \text{pendingUnequip}[h][s_2]$$

### INV-17: Bazaar Escrow Solvency & Liability Coverage
$$\text{GoldBalance}(\text{Bazaar}) \ge \sum \text{bazaarProceedsEscrow} \quad \land \quad \text{HoodBalance}(\text{Bazaar}) \equiv \text{activeListings.length}$$

### INV-18: Gilded Bow Split Cap Invariant
$$\text{forgedGildedBows} \le 750 \quad \land \quad \text{droppedGildedBows} \le 250 \quad \land \quad \text{totalGildedBows} \le 1,000$$
"""
    return content

if __name__ == "__main__":
    content = build_blueprint()
    paths = [
        "/home/arson/rhnftproject/HOODQUEST_MASTER_BLUEPRINT.md",
        "/mnt/c/Users/Eric/Desktop/HOODQUEST_MASTER_BLUEPRINT.md",
        "/mnt/c/Users/Eric/Downloads/HOODQUEST_MASTER_BLUEPRINT.md"
    ]
    for p in paths:
        with open(p, "w") as f:
            f.write(content)
        print(f"Written successfully to {p} ({len(content)} bytes, {len(content.splitlines())} lines)")
