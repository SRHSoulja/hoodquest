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
    root.createDefaultResolver = exports.createDefaultResolver;
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
    createDefaultResolver
  };
}));
