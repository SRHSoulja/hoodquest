// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

enum SupplyMode { UNCAPPED, MAX_LIFETIME, MAX_CIRCULATING, SPLIT }
enum MintSource { DROP, EVENT }
enum EventKind { CASTLE, TAX_TRAIN, JUBILEE, SOLSTICE }
enum ActionKind { CASTLE, TAX_TRAIN, JUBILEE }
enum BazaarTransferMode { NONE, LISTING_DEPOSIT, CANCEL_WITHDRAWAL, SALE_PURCHASE }

struct HeistSnapshot {
    uint8 atk;
    uint8 def;
    uint8 stealth;
    uint16 critBps;
    uint16 goldBonusBps;
    uint16 economicRewardBps;
    bool initialFatigue;
}

struct CombatSnapshot {
    uint8 atk;
    uint8 def;
    uint8 stealth;
    uint16 critBps;
    uint16 goldBonusBps;
    uint16 economicRewardBps;
    bool initialFatigue;
    uint8 morale;
}

struct RewardBundle {
    uint256 gold;
    uint256 yew;
    uint256 iron;
    uint256 baskets;
    uint256 elixirs;
    uint256 gildedBows;
    uint256 yewLongbows;
    uint256 quarterstaffs;
    uint256 poacherDaggers;
}

struct EventConfig {
    bool exists;
    EventKind kind;
    uint32 eventYear;
    uint64 startTime;
    uint64 endTime;
    uint32 cap;
}

struct CraftRecipe {
    bool isValid;
    SupplyMode mode;
    uint256 cap;
    uint256 goldCost;
    uint256 yewCost;
    uint256 ironCost;
}

struct UnequipRequest {
    uint64 maturesAt;
    uint32 itemId;
}
