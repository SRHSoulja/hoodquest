// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import { ERC721 } from "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import { Strings } from "@openzeppelin/contracts/utils/Strings.sol";
import { Base64 } from "@openzeppelin/contracts/utils/Base64.sol";
import { SSTORE2 } from "./utils/SSTORE2.sol";

/**
 * @title HoodQuestCartridge
 * @notice Production multi-chunk compressed on-chain game cartridge.
 * @dev Stores deflate-compressed HTML/JS chunks in SSTORE2 bytecode and serves
 *      an on-chain reconstitution loader inside animation_url.
 */
contract HoodQuestCartridge is ERC721 {
    using Strings for uint256;
    using Strings for address;

    uint256 public constant MAX_CHUNK_SIZE = 24575;

    address[] public cartridgeChunks;
    bytes32 public immutable contentHash; // Keccak-256 of uncompressed payload
    bytes32 public immutable compressedHash; // Keccak-256 of compressed payload
    uint32 public immutable uncompressedSize;
    uint32 public immutable compressedSize;

    constructor(
        address[] memory _chunks,
        bytes32 _contentHash,
        bytes32 _compressedHash,
        uint32 _uncompressedSize,
        uint32 _compressedSize
    ) ERC721("HoodQuest Full On-Chain Cartridge", "HOODGAME") {
        require(_chunks.length > 0, "No chunks provided");

        for (uint256 i = 0; i < _chunks.length; i++) {
            require(_chunks[i] != address(0), "Zero chunk address");
            cartridgeChunks.push(_chunks[i]);
        }

        contentHash = _contentHash;
        compressedHash = _compressedHash;
        uncompressedSize = _uncompressedSize;
        compressedSize = _compressedSize;

        _mint(msg.sender, 1);
    }

    function chunkCount() external view returns (uint256) {
        return cartridgeChunks.length;
    }

    function getChunk(uint256 index) external view returns (bytes memory) {
        require(index < cartridgeChunks.length, "Index out of bounds");
        return SSTORE2.read(cartridgeChunks[index]);
    }

    function getChunkAddresses() external view returns (address[] memory) {
        return cartridgeChunks;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        _requireOwned(tokenId);

        // Build JSON array of chunk addresses: ["0x...", "0x..."]
        bytes memory chunkListBytes = "[";
        for (uint256 i = 0; i < cartridgeChunks.length; i++) {
            if (i > 0) {
                chunkListBytes = abi.encodePacked(chunkListBytes, ",");
            }
            chunkListBytes = abi.encodePacked(
                chunkListBytes,
                '"',
                Strings.toHexString(cartridgeChunks[i]),
                '"'
            );
        }
        chunkListBytes = abi.encodePacked(chunkListBytes, "]");

        // Self-contained on-chain loader with native browser DecompressionStream
        string memory loaderHtml = string(abi.encodePacked(
            '<!DOCTYPE html><html><head><meta charset="utf-8"><title>HoodQuest</title></head>',
            '<body style="margin:0;background:#070d08;color:#a1a1aa;font-family:monospace;display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;">',
            unicode'<div id="status" style="padding:16px;text-align:center;">⚡ Reconstituting HoodQuest from On-Chain Bytecode...</div>',
            '<script>',
            '(()=>{function m(){var s={};return{getItem:k=>s[k]||null,setItem:(k,v)=>{s[k]=String(v)},removeItem:k=>{delete s[k]},clear:()=>{s={}},get length(){return Object.keys(s).length},key:i=>Object.keys(s)[i]||null}}try{window.localStorage}catch(_){try{Object.defineProperty(window,"localStorage",{value:m(),configurable:true,writable:true})}catch(_){}}try{window.sessionStorage}catch(_){try{Object.defineProperty(window,"sessionStorage",{value:m(),configurable:true,writable:true})}catch(_){}}})();',
            '(async()=>{',
            'const status=document.getElementById("status");',
            'try{',
            'const chunks=', string(chunkListBytes), ';',
            'const rpc="https://rpc.testnet.chain.robinhood.com";',
            'const pieces=await Promise.all(chunks.map(async(addr)=>{',
            'for(let attempt=0;attempt<3;attempt++){',
            'try{',
            'const res=await fetch(rpc,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({jsonrpc:"2.0",id:1,method:"eth_getCode",params:[addr,"latest"]})});',
            'if(!res.ok)throw new Error("RPC error "+res.status);',
            'const j=await res.json();',
            'if(!j.result||j.result==="0x")throw new Error("Bytecode chunk unavailable at "+addr);',
            'const hex=j.result.slice(4);',
            'const b=new Uint8Array(hex.length/2);',
            'for(let i=0;i<b.length;i++)b[i]=parseInt(hex.substr(i*2,2),16);',
            'return b;',
            '}catch(err){if(attempt===2)throw err;await new Promise(r=>setTimeout(r,300));}',
            '}',
            '}));',
            'let total=0;for(const p of pieces)total+=p.length;',
            'const full=new Uint8Array(total);let off=0;for(const p of pieces){full.set(p,off);off+=p.length;}',
            'const ds=new DecompressionStream("deflate");',
            'const w=ds.writable.getWriter();w.write(full);w.close();',
            'const html=await new Response(ds.readable).text();',
            'document.open();document.write(html);document.close();',
            '}catch(e){',
            'status.innerText="Cartridge Bytecode Unavailable: "+e.message;',
            'status.style.color="#f87171";',
            '}',
            '})();',
            '</script></body></html>'
        ));

        string memory animationUrl = string(abi.encodePacked(
            "data:text/html;base64,",
            Base64.encode(bytes(loaderHtml))
        ));

        string memory svg = string(abi.encodePacked(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 320" width="100%" height="100%">',
            '<defs><radialGradient id="bg" cx="50%" cy="30%" r="70%"><stop offset="0%" stop-color="#153819"/><stop offset="60%" stop-color="#08150a"/><stop offset="100%" stop-color="#030804"/></radialGradient></defs>',
            '<rect width="320" height="320" fill="url(#bg)"/>',
            '<rect x="10" y="10" width="300" height="300" rx="12" fill="none" stroke="#22c55e" stroke-width="2" opacity="0.6"/>',
            '<circle cx="210" cy="85" r="28" fill="#fef08a" opacity="0.9"/>',
            '<circle cx="218" cy="80" r="26" fill="#153819"/>',
            '<polygon points="40,165 60,115 80,165" fill="#0b2413"/>',
            '<polygon points="75,170 98,105 120,170" fill="#0f331b"/>',
            '<polygon points="115,175 140,95 165,175" fill="#144223"/>',
            '<polygon points="160,170 185,100 210,170" fill="#0f331b"/>',
            '<polygon points="205,175 235,90 265,175" fill="#144223"/>',
            '<ellipse cx="160" cy="180" rx="140" ry="22" fill="#051409"/>',
            '<rect x="146" y="152" width="7" height="20" fill="#15803d"/><rect x="160" y="152" width="7" height="20" fill="#15803d"/>',
            '<rect x="142" y="125" width="28" height="28" fill="#166534"/><rect x="139" y="132" width="34" height="16" fill="#14532d"/>',
            '<rect x="147" y="136" width="18" height="5" fill="#b45309"/><rect x="154" y="136" width="4" height="5" fill="#ffd700"/>',
            '<circle cx="156" cy="115" r="10" fill="#fbcfe8"/>',
            '<polygon points="146,112 168,112 165,100 149,101" fill="#166534"/>',
            '<path d="M162,104 Q172,92 178,98" stroke="#e11d48" stroke-width="3" fill="none"/>',
            '<path d="M132,98 Q120,126 132,154" stroke="#ffd700" stroke-width="4" fill="none"/>',
            '<line x1="132" y1="98" x2="132" y2="154" stroke="#fef08a" stroke-width="2"/>',
            '<line x1="126" y1="126" x2="162" y2="126" stroke="#fff" stroke-width="3"/>',
            '<polygon points="120,126 126,121 126,131" fill="#ffd700"/>',
            '<text x="160" y="235" fill="#ffd700" font-family="Arial Black, Impact, sans-serif" font-weight="900" font-size="24" text-anchor="middle" letter-spacing="2">HOODQUEST</text>',
            '<text x="160" y="258" fill="#86efac" font-family="monospace" font-weight="bold" font-size="11" text-anchor="middle" letter-spacing="1">16-BIT ON-CHAIN LIVING RPG</text>',
            '<rect x="50" y="272" width="220" height="24" rx="6" fill="#15803d" stroke="#4ade80" stroke-width="1.5"/>',
            '<text x="160" y="288" fill="#ffd700" font-family="monospace" font-weight="bold" font-size="11" text-anchor="middle">ROBINHOOD TESTNET (46630)</text>',
            '</svg>'
        ));

        string memory imageUri = string(abi.encodePacked(
            "data:image/svg+xml;base64,",
            Base64.encode(bytes(svg))
        ));

        string memory json = string(abi.encodePacked(
            '{"name":"HoodQuest Full Cartridge #', tokenId.toString(), '",',
            '"description":"Self-contained, fully playable on-chain game cartridge on Robinhood Chain Testnet.",',
            '"image":"', imageUri, '",',
            '"animation_url":"', animationUrl, '",',
            '"attributes":[{"trait_type":"Type","value":"Full Game Cartridge"},',
            '{"trait_type":"Uncompressed Size","value":"', uint256(uncompressedSize).toString(), ' B"},',
            '{"trait_type":"Compressed Size","value":"', uint256(compressedSize).toString(), ' B"},',
            '{"trait_type":"Chunk Count","value":"', cartridgeChunks.length.toString(), '"}]}'
        ));

        return string(abi.encodePacked("data:application/json;base64,", Base64.encode(bytes(json))));
    }
}
