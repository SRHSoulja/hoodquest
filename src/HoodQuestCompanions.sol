// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { ERC721Enumerable } from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import { ReentrancyGuard } from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import { IHoodQuestCompanions } from "./interfaces/IHoodQuestCompanions.sol";
import { IHoodQuest } from "./interfaces/IHoodQuest.sol";
import { IHoodQuestTreasures } from "./interfaces/IHoodQuestTreasures.sol";

contract HoodQuestCompanions is ERC721Enumerable, ReentrancyGuard, IHoodQuestCompanions {
    address public immutable timelock;
    IHoodQuest public immutable hoodContract;
    IHoodQuestTreasures public immutable treasuresContract;

    uint256 public constant MAX_COMPANION_SUPPLY = 10_000;
    uint256 public constant YEW = 16;
    uint256 public constant IRON = 17;

    mapping(uint256 => bool) public genesisAdoptionUsed;
    uint256 public nextHoundId = 1;     // 1..4000
    uint256 public nextFalconId = 4001; // 4001..7000
    uint256 public nextOwlId = 7001;    // 7001..10000

    mapping(uint256 => bytes32) public petSeed;
    mapping(uint256 => uint256) public petXp;
    mapping(uint256 => uint64) public hoodEffectiveAgeAtBond;
    mapping(uint256 => uint64) public accumulatedPetActiveSeconds;

    mapping(uint256 => uint32) public lastForageDay;
    mapping(uint256 => uint256) public pendingForageYew;
    mapping(uint256 => uint256) public pendingForageIron;

    event CompanionAdopted(uint256 indexed hoodId, uint256 indexed petId, uint8 species);
    event PetForaged(uint256 indexed petId, uint256 indexed hoodId, bool dropYew, bool dropIron);
    event ForageClaimed(uint256 indexed hoodId, address indexed recipient, uint256 yew, uint256 iron);

    modifier onlyTimelock() {
        require(msg.sender == timelock, "Not timelock");
        _;
    }
    modifier onlyHoodQuest() {
        require(msg.sender == address(hoodContract), "Not HoodQuest Core");
        _;
    }

    constructor(address timelock_, address hoodContract_, address treasuresContract_)
        ERC721("HoodQuest Companions", "HQPET")
    {
        require(timelock_ != address(0), "Invalid timelock");
        require(hoodContract_ != address(0), "Invalid hood contract");
        require(treasuresContract_ != address(0), "Invalid treasures contract");
        timelock = timelock_;
        hoodContract = IHoodQuest(hoodContract_);
        treasuresContract = IHoodQuestTreasures(treasuresContract_);
    }

    function adoptGenesisPet(uint256 hoodId, uint8 speciesChoice) external returns (uint256 petId) {
        require(hoodContract.ownerOf(hoodId) == msg.sender, "Not Hood owner");
        require(!genesisAdoptionUsed[hoodId], "Genesis pet already adopted for this Hood");
        require(!hoodContract.economicActionsPaused(), "Economic actions paused");
        require(hoodContract.heroSeed(hoodId) != bytes32(0), "Hero seed not finalized");
        
        genesisAdoptionUsed[hoodId] = true;
        
        if (speciesChoice == 0) {
            require(nextHoundId <= 4000, "Hounds exhausted");
            petId = nextHoundId++;
            treasuresContract.burnAdoptionGold(msg.sender, 20);
        } else if (speciesChoice == 1) {
            require(nextFalconId <= 7000, "Falcons exhausted");
            petId = nextFalconId++;
            treasuresContract.burnAdoptionGold(msg.sender, 30);
        } else if (speciesChoice == 2) {
            require(nextOwlId <= 10000, "Owls exhausted");
            petId = nextOwlId++;
            treasuresContract.burnAdoptionGold(msg.sender, 40);
        } else {
            revert("Invalid species");
        }
        
        petSeed[petId] = keccak256(abi.encode(
            hoodContract.heroSeed(hoodId),
            petId,
            speciesChoice,
            address(this),
            block.chainid
        ));
        
        _safeMint(msg.sender, petId);
        emit CompanionAdopted(hoodId, petId, speciesChoice);
    }

    function species(uint256 petId) public pure returns (uint8) {
        require(petId >= 1 && petId <= 10000, "Invalid petId");
        if (petId <= 4000) return 0;
        if (petId <= 7000) return 1;
        return 2;
    }

    function petSpecies(uint256 petId) external pure returns (uint8) {
        return species(petId);
    }

    function effectivePetAge(uint256 petId) public view returns (uint256) {
        uint256 hoodId = hoodContract.petBoundToHood(petId);
        if (hoodId == 0) return accumulatedPetActiveSeconds[petId];
        uint256 hoodCurrentAge = hoodContract.effectiveBiologicalAge(hoodId);
        return accumulatedPetActiveSeconds[petId] + (hoodCurrentAge - hoodEffectiveAgeAtBond[petId]);
    }

    function bondRank(uint256 petId) public view returns (uint8) {
        uint256 xp = petXp[petId];
        if (xp >= 3650) return 5;
        if (xp >= 1800) return 4;
        if (xp >= 900)  return 3;
        if (xp >= 300)  return 2;
        return 1;
    }

    function recordBondAge(uint256 petId, uint64 hoodAge) external onlyHoodQuest {
        hoodEffectiveAgeAtBond[petId] = hoodAge;
    }

    function settleDebondAge(uint256 petId, uint64 hoodAge) external onlyHoodQuest {
        require(hoodEffectiveAgeAtBond[petId] <= hoodAge, "Invalid bond age");
        accumulatedPetActiveSeconds[petId] += (hoodAge - hoodEffectiveAgeAtBond[petId]);
        delete hoodEffectiveAgeAtBond[petId];
    }

    function currentUtcDay() public view returns (uint32) {
        return uint32(block.timestamp / 1 days);
    }

    function soloForage(uint256 petId) external nonReentrant {
        uint256 hoodId = hoodContract.petBoundToHood(petId);
        require(hoodId != 0, "Pet must be bonded to forage");
        require(!hoodContract.isSlumbering(hoodId), "Host Hood is slumbering");
        require(!hoodContract.economicActionsPaused(), "Economic actions paused");
        require(!hoodContract.bazaarEscrowed(hoodId), "Host Hood listed in Bazaar");
        
        address hoodOwner = hoodContract.ownerOf(hoodId);
        require(msg.sender == hoodOwner || hoodContract.isGameDelegate(hoodId, msg.sender), "Not authorized");
        require(lastForageDay[petId] < currentUtcDay(), "Already foraged today");
        
        lastForageDay[petId] = currentUtcDay();
        petXp[petId] += 10; // +10 XP daily forage devotion
        
        bytes32 forageEntropy = keccak256(abi.encode(
            petSeed[petId],
            petId,
            currentUtcDay(),
            address(this),
            block.chainid
        ));
        
        // Deterministic daily drop rates: 12% Yew, 8% Iron
        bool dropYew = uint16(uint256(forageEntropy) % 10_000) < 1200;
        bool dropIron = uint16((uint256(forageEntropy) >> 16) % 10_000) < 800;
        
        if (dropYew) pendingForageYew[hoodId] += 1;
        if (dropIron) pendingForageIron[hoodId] += 1;
        
        emit PetForaged(petId, hoodId, dropYew, dropIron);
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

    function _update(
        address to,
        uint256 tokenId,
        address auth
    ) internal override returns (address from) {
        from = super._update(to, tokenId, auth);

        if (to == address(hoodContract)) {
            require(
                hoodContract.expectedPetDeposit(tokenId) == from,
                "Unsolicited companion vault deposit"
            );
        }
    }
}
