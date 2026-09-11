import os

def generate_blueprint():
    content = r"""# HoodQuest (HQ): Production System Specification (Protocol Frozen V1.0)

A mathematically closed, executable smart contract specification for **HoodQuest (HQ)**, a 100% on-chain living companion RPG with zero backend servers, indexers, or relayers, deployed natively on **Robinhood Chain (Testnet Chain ID 46630, Mainnet Chain ID 4663)**.

- **Official Brand:** **HoodQuest**
- **Shorthand / Ticker:** **HQ**
- **Testnet Subdomain:** `rhtestnethq.gmgnrepeat.com`
- **Future Mainnet Subdomain:** `hq.gmgnrepeat.com`
- **Specification Release:** **Protocol Frozen V1.0 (Production-Ready Specification)**
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

---

## 1. Core Vision & 25-Year Pillars

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

## 2. Smart Contract Topology & Security Architecture

The protocol is divided into specialized contracts to strictly respect Ethereum's 24,576-byte bytecode cap (EIP-170), isolate economic risk, and allow presentation upgrades while keeping economic invariants immutable:

```mermaid
graph TD
    A["HoodQuest.sol (ERC-721 + Enumerable + EIP-4906)<br>Identity, Age, Stamina Counters, Armory Escrow"] 
    B["HoodQuestTreasures.sol (ERC-1155Supply)<br>Royal Gold, Gear, Blacksmith, Rebate Reserve"]
    C["HoodQuestCompanions.sol (ERC-721 + Enumerable)<br>10,000 Pets, Foraging, Bond Ranks"]
    D["HoodQuestRaids.sol (Combat & Action Engine)<br>Heists, Monthly Raids, Tax Train, Jubilees"]
    E["HoodQuestBazaar.sol (Native Camp Bazaar)<br>On-Chain Gold Custody & Loadout Freeze"]
    R["HoodQuestRenderer.sol (Replaceable Engine)<br>Procedural Vector Art & Metadata Strings"]

    A <--> B
    A <--> C
    A <--> D
    B <--> D
    C <--> D
    A <--> E
    B <--> E
    A -.->|staticcall (returndatasize cap)| R
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
  - **Mint Economics & Fresh-Hood Initialization:**
    - Testnet: `MINT_PRICE_WEI = 0` (free test mint); Mainnet: fixed immutable constant (e.g. `0.005 ETH`).
    - Proceeds withdrawable strictly to `PROCEEDS_RECIPIENT` (immutable multisig).
    - Transaction limit: Max 5 mints per transaction.
    - **Fresh-Hood State Initialization:**
      ```solidity
      uint256 id = ++totalHoodsMinted;
      mintTimestamp[id] = uint64(block.timestamp);
      lastCareTimestamp[id] = uint64(block.timestamp);
      lastCareDay[id] = currentUtcDay() - 1; // Allows immediate first-day care
      delegateEpoch[id] = 1;
      rationsUntil[id] = uint64(block.timestamp + 7 days); // 7 days starter rations as state
      slumberAccountedUntil[id] = uint64(block.timestamp);
      seedTargetBlock[id] = ArbSys(0x64).arbBlockNumber() + 2;
      _safeMint(msg.sender, id);
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
            // Fixed non-random fallback: assigns standard genesis trait set
            // Completely eliminates any exploit where players wait out reveal for second roll
            heroSeed[tokenId] = keccak256(abi.encode("STANDARD_GENESIS", tokenId, GENESIS_TIME));
            standardGenesis[tokenId] = true;
        }
        emit HeroSeedFinalized(tokenId, heroSeed[tokenId]);
    }
    ```
    **Economic Gameplay Requirement:** All heists, Castle maneuvers, Boss attacks, and Genesis adoptions strictly require `heroSeed[hoodId] != bytes32(0)`.
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
  - **Delegate Scope & Item Spending:**
    - Authorized delegates may call: `dailyCare`, `feed`, companion `soloForage`, `requestHeistBatch`, `resolveHeist`, `claimHeistRewards` (strictly to `ownerOf(hoodId)`), and `enterCastleHeist`.
    - **Caller Inventory Rule:** When delegates call `feed(hoodId)` or `useElixir(hoodId)`, items are burned **strictly from `msg.sender` (the delegate's own balance)**. Delegates can never spend or burn inventory from the Hood owner.
    - Delegates are **strictly forbidden** from: listing on Bazaar, transferring tokens, equipping items, bonding pets, initiating/finalizing unequips or debonds, and withdrawing assets.
  - **Presentation Upgradeability & Returndata-Protected Fallback:**
    - 48-hour Timelock may replace `renderer` via `setRenderer(address newRenderer)`.
    - Verification guard: `require(newRenderer.code.length > 0, "Invalid renderer code")`.
    - Low-level staticcall with 2,000,000 gas cap and 100,000 byte return limit to prevent memory bloat or malformed ABI reverts:
      ```solidity
      function tokenURI(uint256 tokenId) public view override returns (string memory) {
          _requireOwned(tokenId);
          if (address(renderer) != address(0)) {
              bytes memory callData = abi.encodeWithSelector(IRenderer.tokenURI.selector, tokenId);
              (bool ok, bytes memory data) = address(renderer).staticcall{gas: 2_000_000}(callData);
              if (ok && data.length >= 64 && data.length <= 100_000) {
                  return abi.decode(data, (string));
              }
          }
          return _fallbackTokenURI(tokenId);
      }
      ```

- **`HoodQuestTreasures.sol` (ERC-1155Supply Accounting Authority):**
  - Inherits OpenZeppelin `ERC1155Supply` for authoritative tracking of `totalSupply(id)` (circulating supply).
  - **Supply Modes:**
    ```solidity
    enum SupplyMode { UNCAPPED, MAX_LIFETIME, MAX_CIRCULATING, SPLIT }
    ```
  - **Item Classification:**
    - `ID 1` = `CORE_CURRENCY` (Royal Gold Sovereign)
    - `IDs 2–9, 13–17` = `CORE_ONLY` (Genesis equipment, cloaks, bows, arrows, cornucopias, materials)
    - `IDs 10–12, 18–20` = `RESERVED_UNMINTABLE` (Locked in V1; can only be activated via a one-time Timelock proposal `activateReservedCoreItem()` assigning exclusively to an approved core module).
    - `IDs 21+` = `EXPANSION_REGISTRY` (timelocked registration)
  - **Strict Privilege-Bound Gold Entry Points (No Generic mintGold):**
    1. `mintHeistRewardBundle(address to, RewardBundle bundle)`: callable strictly by resolver-approved Raid engines.
    2. `mintReservedEventGold(address to, uint256 eventId, uint256 amount)`: callable strictly by Raid engine, limited by `eventRecord[eventId].finalBudget`.
    3. `rewardExpansionGold(address to, uint256 amount)`: callable strictly by authorized expansion modules within daily cap.
    4. Bazaar contains zero Gold minting authority; it escrows and transfers existing tokens.
  - **The Blacksmith Crafting State Machine:**
    Detailed in Section 5. Verifies caps before burning, burns Gold through `_burnGold()`, burns materials, updates supply counters, and mints.
  - **Enforceable Soulbound Proof-of-Play (Yew #16 & Iron #17):**
    Checked strictly **before** state modification:
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
  - **Two-Phase Upgrade Authority:**
    `activeRaidEngine` is authorized to create requests and consume stamina.
    `resolverApproved[engine]` retains resolution and reward reservation authority until its pending request counter reaches zero.

- **`HoodQuestBazaar.sol` (Native Camp Bazaar):**
  - Atomic fee burn + proceeds custody escrow. Zero Gold minting authority. Implements `IERC1155Receiver`.
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
    
    // Count active Hood toward the month the heist was INITIATED
    if (req.baseCount > 0) {
        _syncMonthlyActiveHood(req.hoodId, req.monthEpochAtRequest);
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
        // Deterministic fallback: process base roll of 1 through economic pipeline
        // Consumes existing fatigue without triggering new fatigue; 0 materials, 0 rares
        for (uint8 i = 0; i < req.count; i++) {
            _resolveFallbackRoll(req.hoodId, req.snapshot, bundle);
        }
        fatigueActive = false;
        emit HeistFallbackResolved(requestId, req.hoodId, req.count);
    }
    
    hoodContract.setFatigue(req.hoodId, fatigueActive);
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

### 3. Precision Drop-Rate Scale & Explicit Multipliers:
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

Each sub-roll is domain-separated to eliminate correlation:
```solidity
bytes32 goldEntropy = keccak256(abi.encode(rollEntropy, "GOLD"));
bytes32 rareEntropy = keccak256(abi.encode(rollEntropy, "RARE"));
bytes32 matEntropy  = keccak256(abi.encode(rollEntropy, "MATERIALS"));
```

Calculations use `Math.mulDiv`:
```solidity
uint256 effectiveRareChance = Math.mulDiv(
    baseChance,
    combatMultiplierBps * (fatigueActive ? 7500 : 10000) * snapshot.economicRewardBps,
    10_000 * 10_000 * 10_000
);
```

### 4. Starvation & Bonus Gold Fixed-Point Pipeline:
"Base roll of 1–3 Gold before economic modifiers". Starvation and Gold bonuses are processed through an integrated fixed-point carry pipeline:
```solidity
// Step 1: Base roll of 1-3 Gold
uint256 baseRoll = 1 + (uint256(goldEntropy) % 3);

// Step 2: Starvation modifier with carry (5,000 bps starving / 10,000 bps fed)
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

---

## 4. The Armory Escrow Vault & Bazaar Custody Engine

### 1. Aggregate Custody Invariants (ERC-1155 vs. ERC-721):
- **ERC-1155 Equipment Custody:**
  Because ERC-1155 tokens are fungible balances sharing item IDs, reverse binding maps to aggregate vault custody:
  ```solidity
  mapping(uint256 => uint256) public boundCount; // itemId => total bound in vault
  ```
  On `equipItem`: `boundCount[itemId]++`. On `finalizeUnequip`: `boundCount[itemId]--`.
  **Vault Custody Invariant:**
  ```text
  Treasury.balanceOf(HoodQuestVault, itemId) == boundCount[itemId]
  ```
- **ERC-721 Companion Custody:**
  Companions possess unique token IDs, maintaining direct reverse binding: `petBoundToHood[petId] == hoodId`.

### 2. Per-Slot Unequip Requests & Bazaar Pre-Sale Gate:
```solidity
struct UnequipRequest {
    uint64 maturesAt;
    uint32 itemId;
}
mapping(uint256 => mapping(uint8 => UnequipRequest)) public pendingUnequip;
mapping(uint256 => uint8) public pendingUnequipCount;

function canList(uint256 hoodId) public view returns (bool allowed, uint256 reasonFlags) {
    if (pendingGameplayCount[hoodId] > 0) reasonFlags |= 1;
    if (pendingUnequipCount[hoodId] > 0) reasonFlags |= 2;
    if (pendingDebondMaturesAt[hoodId] > 0) reasonFlags |= 4;
    if (hasActiveSolsticeCommitment[hoodId]) reasonFlags |= 8;
    if (pendingEventCount[hoodId] > 0) reasonFlags |= 16;
    if (_hasUnclaimedHeistRewards(hoodId)) reasonFlags |= 32;
    allowed = (reasonFlags == 0);
}
```

### 3. Native Camp Bazaar State Machine (Zero Reminting):
The Bazaar escrows Gold from buyers and holds it in entitlement custody for sellers. Zero Gold is minted during withdrawals:
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

function listHero(uint256 hoodId, uint256 price) external nonReentrant {
    require(price >= 40, "Minimum price is 40 Gold");
    (bool allowed, ) = canList(hoodId);
    require(allowed, "Hood not listable");
    require(hoodContract.ownerOf(hoodId) == msg.sender, "Not owner");
    
    bytes32 hash = hoodContract.getLoadoutHash(hoodId);
    listings[hoodId] = Listing(msg.sender, price, hash);
    
    activeListingTokenIds.push(hoodId);
    activeListingIndexPlusOne[hoodId] = activeListingTokenIds.length;
    
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
    
    // Atomically burn fee and transfer proceeds into Bazaar custody
    treasuresContract.settleBazaarPayment(msg.sender, address(this), l.price, fee);
    
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
    
    // Transfer existing Gold out of Bazaar custody (never mints)
    treasuresContract.safeTransferFrom(address(this), recipient, 1, amount, "");
    emit ProceedsWithdrawn(msg.sender, recipient, amount);
}

function getActiveListings(uint256 cursor, uint256 limit) external view returns (uint256[] memory tokenIds, uint256 nextCursor) {
    require(limit >= 1 && limit <= 100, "Limit must be 1..100");
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

## 5. Anti-Power-Creep Weapon Matrix & The Blacksmith

### Statutory Stat Invariants:
1. `MAX_EFFECTIVE_ATK = 45` (Gilded Bow +20 + Golden Arrow +25 apex).
2. `MAX_EFFECTIVE_DEF = 30` (Locksley Cloak +20 + Camp Hound Rank 5 +10).
3. `MAX_EFFECTIVE_STEALTH = 30` (Twin Daggers +15 + Locksley Cloak +10 + Barn Owl Rank 5 +5).
4. `MAX_EFFECTIVE_MORALE = 10` (Silver Rallying Horn +10 statutory cap).
5. `BASE_COMBAT_POWER = 50` (Baseline for ungeared Hoods).
6. `MAX_GOLD_MULTIPLIER = 40%` (Gilded Bow +20% + Owl Rank 5 +10% + Devotion +10%).
7. `MAX_CRIT_CHANCE = 8%` (Hunting Falcon Rank 5 apex; no unmodeled crit sources).

### Complete Canonical Arsenal & Blacksmith Recipes:

| ID | Item Name | Slot | Supply Mode | Hard Cap | Blacksmith Craft Recipe | Primary Mechanics & Ceilings |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Royal Gold Sovereign** | Currency | `UNCAPPED` | Dynamic | Base Drop | Universal currency (25% rebate / 75% burn) |
| **2** | **Nottingham Mead Cask** | `Decor` | `MAX_CIRCULATING` | **5,000** | 5 🪙 | Campfire banter in SVG |
| **3** | **Gilded Recurve Bow** | `Weapon` | `SPLIT` | **1,000** (750 Forge / 250 Drop) | 60 🪙 + 5 Yew + 5 Iron | **+20 ATK & +20% Gold Multiplier** |
| **4** | **The Golden Arrow** | `Ammo` | `MAX_LIFETIME` | **25** | Event Prize Only | **+25 ATK** (Requires Bow; non-consumable) |
| **5** | **Greenwood Elixir** | Consumable | `MAX_CIRCULATING` | **2,500** | 25 🪙 | **+5 Heists** (Max 1/day; 0% recursive drop) |
| **6** | **Locksley Velvet Cloak** | `Armor` | `MAX_LIFETIME` | **750** | 30 🪙 + 2 Yew + 2 Iron | **+20 DEF & +10 STEALTH** |
| **7** | **Forest Feast Basket** | Sustenance | `UNCAPPED` | Consumable | 14 🪙 | **7-Day Rations:** Max 56d stored; stops starvation |
| **8** | **Silver Rallying Horn** | `Utility` | `MAX_LIFETIME` | **500** | 35 🪙 + 3 Yew + 3 Iron | **+10 MORALE** (Castle Infiltration Aura) |
| **9** | **Friar's Cornucopia** | `SustenanceRelic` | `MAX_LIFETIME`| **25** | 5-Yr Jubilee Only | **Permanent Fed State** (7-day min bind; feeds 1 Hood) |
| **13**| **Yew Forest Longbow** | `Weapon` | `MAX_LIFETIME` | **10,000** | 10 🪙 + 2 Yew | **+10 ATK** (Common Bow) |
| **14**| **Oak Quarterstaff** | `Weapon` | `MAX_LIFETIME` | **2,500** | 20 🪙 + 3 Yew + 1 Iron | **+15 DEF** (Sturdy Brawler Staff) |
| **15**| **Poacher's Twin Daggers**| `Weapon` | `MAX_LIFETIME` | **1,500** | 25 🪙 + 1 Yew + 3 Iron | **+15 STEALTH** (Infiltration Weapon) |
| **16**| **Sherwood Yew (Timber)** | Material | `UNCAPPED` | Soulbound | Quest Drop (25%) | **Proof of Play:** Soulbound timber |
| **17**| **Nottingham Iron (Steel)**| Material | `UNCAPPED` | Soulbound | Quest Drop (20%) | **Proof of Play:** Soulbound steel |

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

### Scarce Reservation & Conversion State Machine:
```solidity
enum MintSource { DROP, EVENT }

function reserveItem(uint256 itemId, MintSource source) external onlyResolver returns (bool) {
    if (itemId == GILDED_BOW) {
        if (droppedGildedBows + dropReservedGildedBows >= 250) return false;
        if (lifetimeMinted[itemId] + reservedUnclaimed[itemId] >= 1000) return false;
        dropReservedGildedBows++;
        reservedUnclaimed[itemId]++;
        return true;
    }
    
    uint256 cap = itemLifetimeCap[itemId];
    if (cap == 0) return true;
    if (lifetimeMinted[itemId] + reservedUnclaimed[itemId] < cap) {
        reservedUnclaimed[itemId]++;
        return true;
    }
    return false;
}

function mintRewardBundle(address to, RewardBundle calldata bundle) external onlyResolver nonReentrant {
    // Atomically decrement reservations, increment lifetime mints, and mint tokens
    if (bundle.gildedBows > 0) {
        dropReservedGildedBows -= bundle.gildedBows;
        reservedUnclaimed[GILDED_BOW] -= bundle.gildedBows;
        droppedGildedBows += bundle.gildedBows;
        lifetimeMinted[GILDED_BOW] += bundle.gildedBows;
        _mint(to, GILDED_BOW, bundle.gildedBows, "");
    }
    if (bundle.gold > 0) {
        _mint(to, 1, bundle.gold, "");
    }
    // Mint common gear, consumables, and materials...
}
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
- **Companion Foraging Executable Rule:**
  ```solidity
  function soloForage(uint256 petId) external nonReentrant {
      uint256 hoodId = petBoundToHood[petId];
      require(hoodId != 0, "Pet must be bonded to forage");
      require(!hoodContract.isSlumbering(hoodId), "Host Hood is slumbering");
      require(!hoodContract.economicActionsPaused(), "Economic actions paused");
      require(msg.sender == ownerOf(petId) || hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
      require(lastForageDay[petId] < currentUtcDay(), "Already foraged today");
      
      lastForageDay[petId] = currentUtcDay();
      petXp[petId] += 10;
      
      bytes32 forageEntropy = keccak256(abi.encode(
          petSeed[petId],
          petId,
          currentUtcDay(),
          address(this),
          block.chainid
      ));
      
      bool dropYew = uint16(uint256(forageEntropy) % 10_000) < 1200; // 12%
      bool dropIron = uint16((uint256(forageEntropy) >> 16) % 10_000) < 800; // 8%
      
      if (dropYew) treasuresContract.mintForageMaterial(msg.sender, YEW, 1);
      if (dropIron) treasuresContract.mintForageMaterial(msg.sender, IRON, 1);
      emit CompanionForaged(petId, hoodId, dropYew, dropIron);
  }
  ```

---

## 7. The Upkeep, Slumber & Calibrated Devotion System

### 1. Daily Care Function & Idempotent Slumber Settlement:
```solidity
function _settleSlumber(uint256 tokenId) internal {
    uint256 careUntil = lastCareTimestamp[tokenId] + 3 days;
    uint256 protectedUntil = careUntil > rationsUntil[tokenId] ? careUntil : rationsUntil[tokenId];
    uint256 start = protectedUntil > slumberAccountedUntil[tokenId] ? protectedUntil : slumberAccountedUntil[tokenId];
    if (block.timestamp > start) {
        completedSlumberSeconds[tokenId] += (block.timestamp - start);
        slumberAccountedUntil[tokenId] = uint64(block.timestamp);
    }
}

function dailyCare(uint256 hoodId) external {
    require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(lastCareDay[hoodId] < currentUtcDay(), "Already cared today");
    _settleSlumber(hoodId);
    lastCareDay[hoodId] = currentUtcDay();
    lastCareTimestamp[hoodId] = uint64(block.timestamp);
    emit DailyCarePerformed(hoodId, currentUtcDay());
}
```

### 2. Starvation & 56-Day Feeding State Machine:
- **Modifier Matrix:**
  - `fed + awake`: `economicRewardBps = 10,000` (100% yields).
  - `starving + awake`: `economicRewardBps = 5,000` (50% penalty with carry).
  - `slumbering`: Heists unavailable (`revert HeroSlumbering`).
- **Feeding Function (Clean 56-Day / 8-Basket Cap):**
  ```solidity
  function feed(uint256 hoodId) external {
      require(msg.sender == ownerOf(hoodId) || isGameDelegate(hoodId, msg.sender), "Not authorized");
      _settleSlumber(hoodId);
      treasuresContract.burnRationBasket(msg.sender, 1);
      
      uint256 currentRations = rationsUntil[hoodId];
      uint256 baseTime = currentRations > block.timestamp ? currentRations : block.timestamp;
      uint256 newRations = baseTime + 7 days;
      require(newRations <= block.timestamp + 56 days, "Max 8 baskets / 56 days prepayment");
      
      rationsUntil[hoodId] = uint64(newRations);
      emit HeroFed(hoodId, newRations);
  }
  ```

### 3. Cornucopia Campfire Care Invariant:
Cornucopia provides permanent fed status (`isFed(hoodId) == true` unconditionally), but does **not** replace daily care. A Hood with a Cornucopia still slumbers if `dailyCare` is neglected for 3 days (`block.timestamp > lastCareTimestamp + 3 days`).

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

### 1. Paper-Doll Generative Traits & Hand Anchoring:
- Natural sloping scapular curves and tapered necks replace rigid block models.
- **Zero Floating Weapons:** All weapons pass directly through the character's hand geometry (`quadraticCurveTo`), with knuckles curled over the riser/grip.
- **Standard Genesis Trait Set:** If a Hood's random seed reveal expires (>256 blocks), `standardGenesis[tokenId] = true` is flagged. The renderer renders a fixed, non-rare standard recruit outfit, eliminating any rarity advantage from deliberately letting the reveal expire.

---

## 9. The Sherwood Astronomical Calendar & World Events Engine

### 1. Sherwood Astronomical Calendar:
```solidity
uint256 elapsed = block.timestamp - GENESIS_TIME;
uint256 worldYearIndex  = elapsed / 365 days; // 0-based
uint256 worldYearNumber = worldYearIndex + 1; // 1-based (Years 1..25+)
uint256 dayOfYear = (elapsed % 365 days) / 1 days;

uint256 monthInYear = dayOfYear < 360 ? dayOfYear / 30 : 11; // Solstice days 360..364 belong to Month-12 epoch
uint256 monthEpoch = worldYearIndex * 12 + monthInYear;
```

### 2. First-Month Epoch Handling & O(1) Active Hood Tracking:
```solidity
mapping(uint256 => uint32) public lastActiveMonthPlusOne;
mapping(uint32 => uint32) public monthlyActiveHoodCount;

function _syncMonthlyActiveHood(uint256 hoodId, uint32 targetMonthEpoch) internal {
    uint32 key = targetMonthEpoch + 1;
    if (lastActiveMonthPlusOne[hoodId] != key) {
        lastActiveMonthPlusOne[hoodId] = key;
        monthlyActiveHoodCount[targetMonthEpoch]++;
    }
}

function getBreachTarget(uint32 epoch) public view returns (uint256) {
    uint256 previousActive = (epoch == 0) ? 0 : monthlyActiveHoodCount[epoch - 1];
    uint256 target = previousActive * 60;
    return target < 1000 ? 1000 : target;
}
```

### 3. Unified Reusable `ActionRequest` Engine:
All major world events (Monthly Castle, Tax Train, and Jubilee) share a single robust state machine:

```solidity
enum ActionKind { CASTLE, TAX_TRAIN, JUBILEE }

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
mapping(uint256 => uint256) public pendingEventCount; // hoodId => pending count for Bazaar

function requestActionEvent(
    uint256 hoodId,
    uint256 eventId,
    ActionKind kind,
    uint8 sector
) external returns (uint256 requestId) {
    require(msg.sender == hoodContract.ownerOf(hoodId) || hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
    require(!hoodContract.isSlumbering(hoodId), "Hero is slumbering");
    require(!hoodContract.economicActionsPaused(), "Paused");
    require(hoodContract.heroSeed(hoodId) != bytes32(0), "Seed not finalized");
    require(isEventActive(eventId), "Event not active");
    require(block.timestamp <= eventEndTime[eventId] - 1 hours, "Action cutoff reached");
    
    _consumeEventAttempt(hoodId, eventId, kind);
    
    if (hoodContribution[eventId][hoodId] == 0) {
        pendingEventCount[hoodId]++;
    }
    
    CombatSnapshot memory snap = hoodContract.captureCombatSnapshot(hoodId);
    requestId = ++nonce;
    uint64 target = uint64(ArbSys(address(0x64)).arbBlockNumber() + 2);
    
    actionRequests[requestId] = ActionRequest(hoodId, eventId, target, kind, sector, snap);
    hoodContract.incrementPendingGameplay(hoodId, 1);
    emit ActionRequested(requestId, hoodId, eventId, kind);
}

function resolveActionEvent(uint256 requestId) external nonReentrant {
    ActionRequest memory req = actionRequests[requestId];
    require(req.targetBlock > 0, "Non-existent request");
    
    uint256 currentBlock = ArbSys(address(0x64)).arbBlockNumber();
    require(currentBlock > req.targetBlock, "Target not reached");
    
    delete actionRequests[requestId];
    hoodContract.decrementPendingGameplay(req.hoodId, 1);
    
    if (currentBlock <= req.targetBlock + 256 && block.timestamp <= eventEndTime[req.eventId] + 2 hours) {
        bytes32 entropy = ArbSys(address(0x64)).arbBlockHash(req.targetBlock);
        uint256 points = _computeEventPoints(req, entropy);
        hoodContribution[req.eventId][req.hoodId] += points;
        totalContribution[req.eventId] += points;
        _updateEventLeaderboard(req.eventId, req.hoodId, points);
        emit ActionResolved(requestId, req.hoodId, points);
    } else {
        // Fallback or past cutoff: 0 points awarded
        emit ActionResolved(requestId, req.hoodId, 0);
    }
}
```

### 4. Event Finalization & Loop-Free Pro-Rata Settlement:
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

function finalizeEvent(uint256 eventId) external nonReentrant {
    require(block.timestamp > eventEndTime[eventId] + 2 hours, "Grace period active");
    EventRecord storage e = eventRecords[eventId];
    require(!e.finalized, "Already finalized");
    
    e.totalContribution = totalContribution[eventId];
    if (e.totalContribution == 0) {
        e.finalBudget = 0;
    } else {
        e.finalBudget = treasuresContract.reserveEventBudget(eventCaps[eventId]);
    }
    e.finalized = true;
    e.claimDeadline = block.timestamp + 90 days;
    
    _reserveEventTrophies(eventId); // Reserves Golden Arrows and Cornucopias
    emit EventFinalized(eventId, e.finalBudget, e.totalContribution);
}

function claimEventReward(uint256 eventId, uint256 hoodId) external nonReentrant {
    require(msg.sender == hoodContract.ownerOf(hoodId), "Not owner");
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp < e.claimDeadline, "Claim window expired");
    require(!eventClaimed[eventId][hoodId], "Already claimed");
    
    uint256 userContribution = hoodContribution[eventId][hoodId];
    require(userContribution > 0, "Zero contribution");
    
    eventClaimed[eventId][hoodId] = true;
    pendingEventCount[hoodId]--;
    
    uint256 reward = (e.finalBudget * userContribution) / e.totalContribution;
    e.claimedTotal += reward;
    
    treasuresContract.mintReservedEventGold(msg.sender, eventId, reward);
    emit EventRewardClaimed(eventId, hoodId, msg.sender, reward);
}

function expireHoodEventParticipation(uint256 eventId, uint256 hoodId) external {
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp >= e.claimDeadline, "Claim window active");
    require(!eventClaimed[eventId][hoodId], "Already claimed");
    require(hoodContribution[eventId][hoodId] > 0, "No participation");
    
    eventClaimed[eventId][hoodId] = true;
    pendingEventCount[hoodId]--;
    emit HoodParticipationExpired(eventId, hoodId);
}

function refundUnclaimedEventBudget(uint256 eventId) external {
    EventRecord storage e = eventRecords[eventId];
    require(e.finalized, "Not finalized");
    require(block.timestamp >= e.claimDeadline, "Claim window active");
    
    uint256 unclaimed = e.finalBudget - e.claimedTotal;
    e.claimedTotal = e.finalBudget;
    
    treasuresContract.refundToRebateReserve(unclaimed);
    emit UnclaimedBudgetRefunded(eventId, unclaimed);
}
```

### 5. Boss Systems & Non-Overlapping Schedule:
- **The Sheriff's Iron Tax Train:**
  - `nextBossThreshold = cumulativeGoldBurned + 150_000` is set **at the conclusion of each cooldown**, requiring fresh Gold burn.
  - **Strict Non-Overlap Rule:** If `block.timestamp + 7 days` would cross into the Jubilee (Day 351) or Solstice (Day 359), the Tax Train activation is queued until Day 1 of the following year.
  - Fixed combat formula: `Power = 50 + ATK + (DEF / 2) + (MORALE * 2)`.
- **The Sherwood Jubilee:**
  - Days 351–357 in Years 5, 10, 15, 20, 25.
  - Rank #1 receives that Jubilee's Golden Arrow; Top 5 receive the 5 Friar's Cornucopias ($5 \times 5 = 25$ total lifetime cap).

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

---

## 11. Master Pre-Flight Audit & Verification Lifecycle Matrix

### Engineering Verification Lifecycle:
All audit items must be tracked across the formal verification lifecycle:
`Specified` -> `Implemented` -> `Unit Tested` -> `Fuzz Tested` -> `Invariant Tested` -> `Testnet Verified` -> `Independently Reviewed` -> `Mainnet Ready`.

| Security Domain | Vulnerability / Threat | Proposed On-Chain Defense Mechanism | Engineering Status |
| :--- | :--- | :--- | :--- |
| **Bazaar Gold Custody** | Burn/mint in Bazaar creating insolvency risk | **Atomic Fee Burn & Escrow:** Burn fee only; transfer proceeds into Bazaar custody; withdrawal transfers held tokens. | `[Specified]` |
| **Aggregate ERC-1155 Custody** | Invariant INV-15 failing on fungible items | **boundCount Mapping:** Tracks total bound per itemId; verifies Vault balance == boundCount[itemId]. | `[Specified]` |
| **Supply Mode Enforcement** | Circulating caps treated as lifetime caps | **SupplyMode Enum:** Tracks MAX_LIFETIME vs MAX_CIRCULATING using OpenZeppelin ERC1155Supply. | `[Specified]` |
| **Gilded Bow 250 Drop Cap** | Forge crafters exhausting drop slots | **Split Cap Enforcement:** reserveItem checks droppedGildedBows < 250; craft checks forgedGildedBows < 750. | `[Specified]` |
| **Reservation Claim Atomicity** | Scarce reservations drifting from mint state | **mintRewardBundle Conversion:** Atomically decrements reservation and increments lifetime/source mints. | `[Specified]` |
| **Concrete ActionRequest Engine** | Unimplemented bespoke combat engines | **Unified ActionRequest:** Reusable engine for Castle, Tax Train, and Jubilee with fixed formulas and cutoff. | `[Specified]` |
| **Executable Event Finalization** | Missing event budget reservation function | **finalizeEvent Function:** Reserves budget, sets deadline, reserves trophies; dedicated mintReservedEventGold. | `[Specified]` |
| **No Generic mintGold** | Unbounded external Gold creation paths | **Privilege-Bound Entry Points:** Dedicated entry points for heists, events, expansions; Bazaar mints nothing. | `[Specified]` |
| **Two-Phase Raid Permissions** | Upgrades stranding V1 resolver reservations | **Active vs Resolver Permissions:** activeRaidEngine creates requests; resolverApproved settles rewards. | `[Specified]` |
| **First-Month Epoch Tracking** | Month 0 defaulting to uncounted; underflow | **lastActiveMonthPlusOne:** Epoch+1 sentinel prevents zero collision; previous active defaults to 0 in Month 0. | `[Specified]` |
| **Fallback Economic Fidelity** | Fallback rolls bypassing starvation carry | **Fallback Pipeline:** Processes base roll of 1 through economic carry pipeline; clears initial fatigue. | `[Specified]` |
| **Precision Drop Scale** | Sub-basis-point drop rates truncating to zero | **1e9 DROP_SCALE & Math.mulDiv:** Precise integer math; domain-separated sub-rolls eliminate correlation. | `[Specified]` |
| **Fresh-Hood Initialization** | New Hoods starting with 0 rations / starving | **Mint Init:** Sets mintTimestamp, careDay-1, delegateEpoch=1, and 7 days starter rations as state. | `[Specified]` |
| **Idempotent Slumber Settlement** | Repeated settlement double-counting sleep | **slumberAccountedUntil:** Accounts sleep strictly from max(protectedUntil, accountedUntil) to now. | `[Specified]` |
| **Event Participation Bazaar Gate** | Pending event participation permanently blocking | **pendingEventCount & Expiration:** Decrements on claim; expireHoodEventParticipation unblocks after 90 days. | `[Specified]` |
| **Clean V1 Combat Bounds** | Unimplemented STUN and archetype mechanics | **Simplified V1 Bounds:** MAX_MORALE = 10; MAX_CRIT = 8%; Quarterstaff is +15 DEF. | `[Specified]` |
| **Tax Train Backlog & Overlap** | Backlog skipping threshold; festival collision | **Fresh Threshold & Queuing:** Next threshold set at cooldown end; Tax Train queued if running into festivals. | `[Specified]` |
| **Event Action Cutoff Grace** | Pending actions straddling finalization | **Cutoff Rules:** Actions stop 1h before event end; 2h resolution grace; 0 points awarded past cutoff. | `[Specified]` |
| **Companion Foraging Authorization** | Unbonded pet farms printing materials | **Bonded-Only Forage:** Pet must be bonded to awake Hood; caller must be owner or delegate. | `[Specified]` |
| **Reserved Core Item Policy** | Ambiguity over reserved items 10-12, 18-20 | **Permanently Unmintable in V1:** Can only be activated via dedicated one-time Timelock proposal. | `[Specified]` |
| **Fixed Fallback Trait Set** | Fallback seed generating alternative rare traits | **standardGenesis Flag:** Renderer renders fixed standard recruit traits if reveal window expired. | `[Specified]` |
| **Bazaar Pagination Safety** | Zero limit causing infinite loops; index collision | **1..100 Limit & IndexPlusOne:** Bounded discovery; indexPlusOne provides clean 0 sentinel. | `[Specified]` |
| **Renderer Returndata Protection** | Massive returndata crashing tokenURI | **returndatasize Bound:** Staticcall with 2M gas cap verifies data length <= 100,000 bytes before decoding. | `[Specified]` |
| **Pristine Plaintext Invariants** | Mangled LaTeX escapes confusing Codex | **Plaintext Fenced Blocks:** Critical invariants formatted in clean Solidity-like plaintext expressions. | `[Specified]` |

---

## 12. Mainnet Acceptance Test & Invariant Specification

Before promoting this specification to Mainnet deployment, the smart contracts must satisfy these 18 formal mathematical invariants in Foundry unit and fuzz test suites:

### INV-1: Hood Token Supply & ID Invariant
```solidity
totalHoodsMinted <= 10_000 && forall id in minted: (1 <= id && id <= 10_000)
```

### INV-2: Mythic Grail Lifetime Mint Ceilings
```solidity
lifetimeMinted[4] + reservedUnclaimed[4] <= 25 &&
lifetimeMinted[9] + reservedUnclaimed[9] <= 25
```

### INV-3: Companion Genesis Parity & Adoption Limit
```solidity
forall hoodId: genesisAdoptionCount[hoodId] <= 1 &&
totalCompanionsMinted <= 10_000
```

### INV-4: Identity-Bound Temporal Tracking
```solidity
forall transfer(from, to, tokenId):
    staminaPost(tokenId) == staminaPre(tokenId) &&
    rationsUntilPost(tokenId) == rationsUntilPre(tokenId)
```

### INV-5: Starvation Economic Multiplier Clamp
```solidity
if (isSlumbering(h)) economicRewardBps == 0;
else if (isFed(h))   economicRewardBps == 10_000;
else                 economicRewardBps == 5_000;
```

### INV-6: Slumbering Action Prohibition
```solidity
forall h: isSlumbering(h) ==> (requestHeistBatch reverts HeroSlumbering)
```

### INV-7: Bounded Expansion Emission Ceiling
```solidity
allocatedAuthorizedDailyCap <= 25_000 // Gold per day
```

### INV-8: Armory Vault Custody Integrity
```solidity
forall slot in BoundSlots: withdrawItem(h, slot) transfers strictly to ownerOf(h)
```

### INV-9: Global Rebate Reserve Solvency
```solidity
totalEventGoldMinted <= cumulativeGoldBurned * 25 / 100
```

### INV-10: Delayed Entropy Terminal State Guarantee
```solidity
forall request: exists terminalState in {Resolved, FallbackResolved}
```

### INV-11: Mixed Stamina Batch Roll Classification
```solidity
forall i < baseCount: isBonusRoll(i) == false;
forall i >= baseCount: isBonusRoll(i) == true && elixirDropChance(i) == 0;
```

### INV-12: Single Pending Heist Batch Invariant
```solidity
forall h: pendingNormalHeist(h) ==> (requestHeistBatch reverts)
```

### INV-13: Delegate Asset Non-Redirection & Inventory Spending
```solidity
forall delegateCalls:
    claimHeistRewards transfers strictly to ownerOf(h) &&
    burnBasket/Elixir burns strictly from msg.sender
```

### INV-14: Scarce-Reward Reservation Solvency
```solidity
forall itemId: lifetimeMinted[itemId] + reservedUnclaimed[itemId] <= itemCap[itemId]
```

### INV-15: Aggregate ERC-1155 Vault Custody
```solidity
forall itemId: Treasury.balanceOf(HoodQuestVault, itemId) == boundCount[itemId]
```

### INV-16: Per-Slot Unequip Request Isolation
```solidity
forall slot1 != slot2: pendingUnequip[h][slot1] is independent of pendingUnequip[h][slot2]
```

### INV-17: Bazaar Escrow Solvency & Liability Coverage
```solidity
Treasury.balanceOf(Bazaar, 1) >= sum(bazaarProceedsEscrow) &&
HoodQuest.balanceOf(Bazaar) == activeListingTokenIds.length
```

### INV-18: Gilded Bow Split Cap Invariant
```solidity
forgedGildedBows <= 750 &&
droppedGildedBows + dropReservedGildedBows <= 250 &&
lifetimeMinted[3] + reservedUnclaimed[3] <= 1000
```
"""
    return content

if __name__ == "__main__":
    content = generate_blueprint()
    paths = [
        "/home/arson/rhnftproject/HOODQUEST_MASTER_BLUEPRINT.md",
        "/mnt/c/Users/Eric/Desktop/HOODQUEST_MASTER_BLUEPRINT.md",
        "/mnt/c/Users/Eric/Downloads/HOODQUEST_MASTER_BLUEPRINT.md"
    ]
    for p in paths:
        with open(p, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Written successfully to {p} ({len(content)} bytes, {len(content.splitlines())} lines)")
