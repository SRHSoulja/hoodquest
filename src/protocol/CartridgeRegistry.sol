// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title CartridgeRegistry
 * @notice On-chain registry tracking cartridge identities, immutable releases, and mutable channels.
 * @dev Enforces strict separation between immutable releases (manifest digests) and mutable channels (e.g. stable, latest).
 */
contract CartridgeRegistry {
    struct Release {
        bytes32 manifestDigest;
        uint64 publishedAt;
        string version;
    }

    struct CartridgeMeta {
        address owner;
        string name;
        uint256 releaseCount;
    }

    /// @notice Standard channel keys
    bytes32 public constant CHANNEL_STABLE = keccak256("stable");
    bytes32 public constant CHANNEL_LATEST = keccak256("latest");
    bytes32 public constant CHANNEL_BETA = keccak256("beta");

    /// @notice Cartridge metadata keyed by unique cartridgeId
    mapping(bytes32 => CartridgeMeta) public cartridges;

    /// @notice Releases list keyed by cartridgeId
    mapping(bytes32 => Release[]) internal _releases;

    /// @notice Current release index pointed to by a channel: cartridgeId => channelKey => releaseIndex
    mapping(bytes32 => mapping(bytes32 => uint256)) public channelReleaseIndex;

    /// @notice Whether a channel has been explicitly assigned: cartridgeId => channelKey => isConfigured
    mapping(bytes32 => mapping(bytes32 => bool)) public channelConfigured;

    // Events
    event CartridgeRegistered(bytes32 indexed cartridgeId, address indexed owner, string name);
    event ReleasePublished(bytes32 indexed cartridgeId, uint256 indexed releaseIndex, string version, bytes32 manifestDigest);
    event ChannelUpdated(bytes32 indexed cartridgeId, bytes32 indexed channelKey, uint256 releaseIndex, bytes32 manifestDigest);
    event CartridgeOwnershipTransferred(bytes32 indexed cartridgeId, address indexed previousOwner, address indexed newOwner);

    // Errors
    error CartridgeAlreadyExists(bytes32 cartridgeId);
    error CartridgeNotFound(bytes32 cartridgeId);
    error Unauthorized(bytes32 cartridgeId, address caller);
    error InvalidOwner();
    error InvalidManifestDigest();
    error InvalidVersion();
    error ReleaseNotFound(bytes32 cartridgeId, uint256 releaseIndex);
    error ChannelNotSet(bytes32 cartridgeId, bytes32 channelKey);

    modifier onlyOwner(bytes32 cartridgeId) {
        address owner = cartridges[cartridgeId].owner;
        if (owner == address(0)) revert CartridgeNotFound(cartridgeId);
        if (owner != msg.sender) revert Unauthorized(cartridgeId, msg.sender);
        _;
    }

    /**
     * @notice Registers a new cartridge namespace.
     * @param name Human-readable identifier/name of the cartridge.
     * @return cartridgeId Unique bytes32 identifier derived from publisher address and name.
     */
    function registerCartridge(string calldata name) external returns (bytes32 cartridgeId) {
        cartridgeId = keccak256(abi.encodePacked(msg.sender, name));
        if (cartridges[cartridgeId].owner != address(0)) {
            revert CartridgeAlreadyExists(cartridgeId);
        }

        cartridges[cartridgeId] = CartridgeMeta({
            owner: msg.sender,
            name: name,
            releaseCount: 0
        });

        emit CartridgeRegistered(cartridgeId, msg.sender, name);
    }

    /**
     * @notice Publishes an immutable release for a cartridge.
     * @param cartridgeId The ID of the cartridge.
     * @param version Semantic version string (e.g. "1.0.0").
     * @param manifestDigest The keccak256 digest of the canonical manifest stored in ContentStore.
     * @return releaseIndex Index of the published release.
     */
    function publishRelease(
        bytes32 cartridgeId,
        string calldata version,
        bytes32 manifestDigest
    ) external onlyOwner(cartridgeId) returns (uint256 releaseIndex) {
        if (manifestDigest == bytes32(0)) revert InvalidManifestDigest();
        if (bytes(version).length == 0) revert InvalidVersion();

        releaseIndex = _releases[cartridgeId].length;

        _releases[cartridgeId].push(Release({
            manifestDigest: manifestDigest,
            publishedAt: uint64(block.timestamp),
            version: version
        }));

        cartridges[cartridgeId].releaseCount = releaseIndex + 1;

        emit ReleasePublished(cartridgeId, releaseIndex, version, manifestDigest);

        // Always update CHANNEL_LATEST to newest release
        channelReleaseIndex[cartridgeId][CHANNEL_LATEST] = releaseIndex;
        channelConfigured[cartridgeId][CHANNEL_LATEST] = true;
        emit ChannelUpdated(cartridgeId, CHANNEL_LATEST, releaseIndex, manifestDigest);

        // If this is the first release (index 0), initialize CHANNEL_STABLE automatically
        if (releaseIndex == 0) {
            channelReleaseIndex[cartridgeId][CHANNEL_STABLE] = 0;
            channelConfigured[cartridgeId][CHANNEL_STABLE] = true;
            emit ChannelUpdated(cartridgeId, CHANNEL_STABLE, 0, manifestDigest);
        }
    }

    /**
     * @notice Points a mutable channel to an existing immutable release.
     * @param cartridgeId The ID of the cartridge.
     * @param channelKey Channel identifier (e.g. CHANNEL_STABLE, CHANNEL_BETA).
     * @param releaseIndex Index of the release to point to.
     */
    function setChannel(
        bytes32 cartridgeId,
        bytes32 channelKey,
        uint256 releaseIndex
    ) external onlyOwner(cartridgeId) {
        if (releaseIndex >= _releases[cartridgeId].length) {
            revert ReleaseNotFound(cartridgeId, releaseIndex);
        }

        channelReleaseIndex[cartridgeId][channelKey] = releaseIndex;
        channelConfigured[cartridgeId][channelKey] = true;

        bytes32 digest = _releases[cartridgeId][releaseIndex].manifestDigest;
        emit ChannelUpdated(cartridgeId, channelKey, releaseIndex, digest);
    }

    /**
     * @notice Transfers ownership of a cartridge.
     */
    function transferOwnership(bytes32 cartridgeId, address newOwner) external onlyOwner(cartridgeId) {
        if (newOwner == address(0)) revert InvalidOwner();
        address previous = cartridges[cartridgeId].owner;
        cartridges[cartridgeId].owner = newOwner;
        emit CartridgeOwnershipTransferred(cartridgeId, previous, newOwner);
    }

    /**
     * @notice Resolves the manifest digest for a specific channel (e.g. CHANNEL_STABLE).
     */
    function resolveManifest(bytes32 cartridgeId, bytes32 channelKey) external view returns (bytes32 manifestDigest) {
        if (cartridges[cartridgeId].owner == address(0)) revert CartridgeNotFound(cartridgeId);
        if (!channelConfigured[cartridgeId][channelKey]) revert ChannelNotSet(cartridgeId, channelKey);

        uint256 index = channelReleaseIndex[cartridgeId][channelKey];
        return _releases[cartridgeId][index].manifestDigest;
    }

    /**
     * @notice Retrieves release by index.
     */
    function getRelease(bytes32 cartridgeId, uint256 releaseIndex) external view returns (Release memory) {
        if (releaseIndex >= _releases[cartridgeId].length) revert ReleaseNotFound(cartridgeId, releaseIndex);
        return _releases[cartridgeId][releaseIndex];
    }

    /**
     * @notice Retrieves total release count for a cartridge.
     */
    function getReleaseCount(bytes32 cartridgeId) external view returns (uint256) {
        return _releases[cartridgeId].length;
    }

    /**
     * @notice Retrieves release by channel key.
     */
    function getChannelRelease(bytes32 cartridgeId, bytes32 channelKey)
        external
        view
        returns (Release memory release, uint256 releaseIndex)
    {
        if (cartridges[cartridgeId].owner == address(0)) revert CartridgeNotFound(cartridgeId);
        if (!channelConfigured[cartridgeId][channelKey]) revert ChannelNotSet(cartridgeId, channelKey);

        releaseIndex = channelReleaseIndex[cartridgeId][channelKey];
        release = _releases[cartridgeId][releaseIndex];
    }
}
