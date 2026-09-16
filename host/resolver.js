/**
 * Console Runtime V0.1 - Cartridge Resolver Interface & Local Implementation
 *
 * Provides clean decoupling between cartridge resolution and the host console.
 * Enables replacing LocalCartridgeResolver with OnchainCartridgeResolver in future stages
 * without modifying any host console logic.
 */

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    const exports = factory();
    root.CartridgeResolver = exports.CartridgeResolver;
    root.LocalCartridgeResolver = exports.LocalCartridgeResolver;
    root.OnchainCartridgeResolver = exports.OnchainCartridgeResolver;
    root.createDefaultResolver = exports.createDefaultResolver;
    root.decodeAbiBytes = exports.decodeAbiBytes;
  }
}(typeof self !== 'undefined' ? self : this, function() {

  /**
   * Abstract Cartridge Resolver
   * Defines formal contract for resolving cartridge metadata and package data.
   */
  class CartridgeResolver {
    /**
     * Resolves a cartridge descriptor and returns package fetching handle
     * @param {string} cartridgeId - Unique identifier or URI
     * @param {object} [options]
     * @returns {Promise<ResolvedCartridge>}
     */
    async resolve(cartridgeId, options = {}) {
      throw new Error('resolve() must be implemented by CartridgeResolver subclass');
    }

    /**
     * Lists available cartridges in this resolver catalog
     * @returns {Promise<Array<{id: string, name: string, version: string, author?: string}>>}
     */
    async listCartridges() {
      throw new Error('listCartridges() must be implemented by CartridgeResolver subclass');
    }
  }

  /**
   * Local Cartridge Resolver
   * Resolves cartridges from local disk, relative paths, or static registry maps.
   */
  class LocalCartridgeResolver extends CartridgeResolver {
    constructor(options = {}) {
      super();
      this.basePath = options.basePath || '../cartridges';
      this.registry = new Map();

      if (options.initialRegistry) {
        for (const [id, desc] of Object.entries(options.initialRegistry)) {
          this.register(id, desc);
        }
      }
    }

    /**
     * Registers a cartridge descriptor in the local catalog
     */
    register(id, descriptor) {
      this.registry.set(id.toLowerCase(), {
        id,
        ...descriptor
      });
    }

    /**
     * Lists all registered cartridges
     */
    async listCartridges() {
      const list = [];
      for (const [id, desc] of this.registry.entries()) {
        list.push({
          id: desc.id || id,
          name: desc.name || desc.manifest?.name || id,
          version: desc.version || desc.manifest?.version || '1.0.0',
          author: desc.author || desc.manifest?.metadata?.author || 'Unknown'
        });
      }
      return list;
    }

    /**
     * Resolves manifest and creates package retrieval delegate
     */
    async resolve(cartridgeId) {
      if (!cartridgeId) {
        throw new Error('Cartridge ID is required for resolution');
      }

      const normId = cartridgeId.toLowerCase();
      const descriptor = this.registry.get(normId);

      // A. If pre-registered with inline manifest
      if (descriptor && descriptor.manifest) {
        const manifest = descriptor.manifest;
        const fetchPackageBytes = async () => {
          if (descriptor.rawBytes) {
            return descriptor.rawBytes;
          }
          const pkgPath = descriptor.packageUri || `${this.basePath}/${normId}/${manifest.entry || 'index.html'}`;
          return await this._fetchText(pkgPath);
        };

        return {
          id: descriptor.id || normId,
          name: manifest.name || descriptor.name || normId,
          version: manifest.version || descriptor.version || '0.1.0',
          release: descriptor.release || 'latest',
          manifest,
          expectedContentHash: manifest.integrity?.contentHash || descriptor.expectedContentHash,
          runtimeRequirement: manifest.runtime?.version || '^0.1.0',
          fetchPackageBytes
        };
      }

      // B. Dynamic relative filesystem / HTTP fetch
      const manifestUri = descriptor?.manifestUri || `${this.basePath}/${normId}/cartridge.json`;
      const manifestText = await this._fetchText(manifestUri);
      let manifest;
      try {
        manifest = JSON.parse(manifestText);
      } catch (e) {
        throw new Error(`Invalid JSON manifest for cartridge "${normId}": ${e.message}`);
      }

      const fetchPackageBytes = async () => {
        const entry = manifest.entry || 'index.html';
        const pkgUri = descriptor?.packageUri || `${this.basePath}/${normId}/${entry}`;
        return await this._fetchText(pkgUri);
      };

      return {
        id: manifest.id || normId,
        name: manifest.name || normId,
        version: manifest.version || '0.1.0',
        release: descriptor?.release || 'latest',
        manifest,
        expectedContentHash: manifest.integrity?.contentHash,
        runtimeRequirement: manifest.runtime?.version || '^0.1.0',
        fetchPackageBytes
      };
    }

    async _fetchText(uri) {
      // Browser environment or remote HTTP/HTTPS resource
      if (typeof window !== 'undefined' || uri.startsWith('http://') || uri.startsWith('https://')) {
        const resp = await fetch(uri);
        if (!resp.ok) {
          throw new Error(`Failed to fetch resource at "${uri}" (HTTP ${resp.status})`);
        }
        return await resp.text();
      }

      // Node.js fs Fallback (for automated tests and CLI)
      if (typeof require === 'function') {
        const fs = require('fs');
        const path = require('path');
        const resolved = path.isAbsolute(uri) ? uri : path.resolve(process.cwd(), uri.replace(/^\.\.\//, ''));
        if (!fs.existsSync(resolved)) {
          throw new Error(`File not found at resolved path: ${resolved}`);
        }
        return fs.readFileSync(resolved, 'utf8');
      }

      throw new Error(`No fetch or filesystem transport available to read "${uri}"`);
    }
  }

  /**
   * Helper to decode ABI-encoded dynamic bytes from eth_call
   */
  function decodeAbiBytes(hexStr) {
    if (!hexStr || hexStr === '0x') return '';
    const clean = hexStr.startsWith('0x') ? hexStr.slice(2) : hexStr;
    if (clean.length < 128) return '';
    const offset = parseInt(clean.slice(0, 64), 16) * 2;
    const len = parseInt(clean.slice(offset, offset + 64), 16);
    const dataHex = clean.slice(offset + 64, offset + 64 + len * 2);
    if (typeof Buffer !== 'undefined') {
      return Buffer.from(dataHex, 'hex').toString('utf8');
    }
    let str = '';
    for (let i = 0; i < dataHex.length; i += 2) {
      str += String.fromCharCode(parseInt(dataHex.substr(i, 2), 16));
    }
    return str;
  }

  /**
   * Onchain Cartridge Resolver
   * Resolves cartridges from on-chain CartridgeRegistry and ContentStore contracts.
   * Enforces cryptographic integrity of manifest and assembled package chunks.
   */
  class OnchainCartridgeResolver extends CartridgeResolver {
    constructor(options = {}) {
      super();
      this.registryAddress = (options.registryAddress || '').toLowerCase();
      this.storeAddress = (options.storeAddress || '').toLowerCase();
      this.rpcUrl = options.rpcUrl || 'https://rpc.ankr.com/eth_sepolia';
      this.callHandler = options.callHandler || null;
      this.channel = options.channel || 'stable';
      this.keccakFn = options.keccakFn || (typeof require === 'function' ? require('js-sha3').keccak256 : (typeof window !== 'undefined' ? window.keccak256 : null));
      this.catalog = new Map();
    }

    registerOnchainCartridge(id, meta) {
      this.catalog.set(id.toLowerCase(), { id, ...meta });
    }

    async listCartridges() {
      const list = [];
      for (const [id, meta] of this.catalog.entries()) {
        list.push({
          id,
          name: meta.name || id,
          version: meta.version || 'onchain',
          author: meta.publisher || 'On-chain'
        });
      }
      return list;
    }

    async _ethCall(to, data) {
      if (this.callHandler) {
        return await this.callHandler({ to, data });
      }
      if (typeof window !== 'undefined' && window.ethereum && window.ethereum.request) {
        return await window.ethereum.request({
          method: 'eth_call',
          params: [{ to, data }, 'latest']
        });
      }
      if (typeof fetch === 'function') {
        const resp = await fetch(this.rpcUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'eth_call',
            params: [{ to, data }, 'latest']
          })
        });
        const json = await resp.json();
        if (json.error) throw new Error(json.error.message || 'RPC Call Failed');
        return json.result;
      }
      throw new Error('No RPC transport available for on-chain call');
    }

    async resolve(cartridgeId, options = {}) {
      if (!cartridgeId) throw new Error('Cartridge ID is required');

      const normId = cartridgeId.toLowerCase();
      const meta = this.catalog.get(normId);

      // Determine 32-byte cartridge identifier
      let cartridgeBytes32 = meta?.cartridgeBytes32;
      if (!cartridgeBytes32) {
        if (normId.startsWith('0x') && normId.length === 66) {
          cartridgeBytes32 = normId;
        } else if (this.keccakFn) {
          cartridgeBytes32 = '0x' + this.keccakFn(normId);
        } else {
          throw new Error(`Cannot compute cartridge identifier hash for: ${cartridgeId}`);
        }
      }

      // Determine channel key
      const channelName = options.channel || this.channel;
      let channelKey = options.channelKey;
      if (!channelKey) {
        channelKey = '0x' + this.keccakFn(channelName);
      }

      // 1. Query CartridgeRegistry.resolveManifest(bytes32,bytes32) -> bytes32 manifestDigest
      // Selector: 0x06fa0577
      const cleanCartId = cartridgeBytes32.startsWith('0x') ? cartridgeBytes32.slice(2).padStart(64, '0') : cartridgeBytes32.padStart(64, '0');
      const cleanChanKey = channelKey.startsWith('0x') ? channelKey.slice(2).padStart(64, '0') : channelKey.padStart(64, '0');
      const resolveCalldata = '0x06fa0577' + cleanCartId + cleanChanKey;

      const manifestDigestHex = await this._ethCall(this.registryAddress, resolveCalldata);
      if (!manifestDigestHex || manifestDigestHex === '0x' || /^0x0+$/.test(manifestDigestHex)) {
        throw new Error(`Cartridge "${cartridgeId}" not found or channel "${channelName}" not configured`);
      }
      const manifestDigest = '0x' + manifestDigestHex.slice(-64).toLowerCase();

      // 2. Query ContentStore.read(bytes32 manifestDigest) -> bytes manifestJson
      // Selector: 0x61da1439
      const readCalldata = '0x61da1439' + manifestDigest.slice(2);
      const manifestBytesHex = await this._ethCall(this.storeAddress, readCalldata);
      const manifestText = decodeAbiBytes(manifestBytesHex);

      if (!manifestText) {
        throw new Error(`Manifest bytes could not be retrieved from ContentStore for digest: ${manifestDigest}`);
      }

      // 3. Verify Manifest Integrity
      const computedManifestDigest = ('0x' + this.keccakFn(manifestText)).toLowerCase();
      if (computedManifestDigest !== manifestDigest) {
        throw new Error(`Manifest integrity verification failed! Expected ${manifestDigest}, computed ${computedManifestDigest}`);
      }

      const manifest = JSON.parse(manifestText);

      // 4. Resolve Entry Point & Chunks
      const entry = manifest.entry || {};
      const expectedContentHash = (entry.digest || manifest.integrity?.contentHash || '').toLowerCase();
      const chunks = entry.chunks || (expectedContentHash ? [expectedContentHash] : []);

      return {
        id: manifest.id || cartridgeId,
        name: manifest.name || cartridgeId,
        version: manifest.version || '1.0.0',
        manifest,
        runtimeRequirement: manifest.runtime?.version || '^0.2.0',
        expectedContentHash,
        fetchPackageBytes: async () => {
          if (chunks.length === 1) {
            const chunkCalldata = '0x61da1439' + chunks[0].slice(2);
            const chunkBytesHex = await this._ethCall(this.storeAddress, chunkCalldata);
            const packageBytes = decodeAbiBytes(chunkBytesHex);
            return packageBytes;
          } else if (chunks.length > 1) {
            let fullData = '';
            for (const c of chunks) {
              const chunkCalldata = '0x61da1439' + c.slice(2);
              const chunkBytesHex = await this._ethCall(this.storeAddress, chunkCalldata);
              fullData += decodeAbiBytes(chunkBytesHex);
            }
            return fullData;
          }
          throw new Error(`No entry chunks defined in manifest for cartridge: ${cartridgeId}`);
        }
      };
    }
  }

  /**
   * Factory function creating standard local resolver preloaded with reference cartridges
   */
  function createDefaultResolver(basePath = '../cartridges') {
    const resolver = new LocalCartridgeResolver({ basePath });

    // Pre-register Cartridge #0001 (HoodQuest)
    resolver.register('hoodquest', {
      id: 'hoodquest',
      name: 'HoodQuest: Sanctuary of the Falcon',
      version: '1.0.0',
      author: 'SRHSoulja',
      manifestUri: `${basePath}/hoodquest/cartridge.json`,
      packageUri: `${basePath}/hoodquest/index.html`
    });

    // Pre-register Cartridge #0002 (Runtime Test Cartridge)
    resolver.register('runtime-test-cartridge', {
      id: 'runtime-test-cartridge',
      name: 'Runtime Test Cartridge',
      version: '0.1.0',
      author: 'Console Development Team',
      manifestUri: `${basePath}/runtime-test-cartridge/cartridge.json`,
      packageUri: `${basePath}/runtime-test-cartridge/index.html`
    });

    return resolver;
  }

  return {
    CartridgeResolver,
    LocalCartridgeResolver,
    OnchainCartridgeResolver,
    createDefaultResolver,
    decodeAbiBytes
  };
}));
