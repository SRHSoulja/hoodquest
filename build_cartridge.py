import zlib, json
from Crypto.Hash import keccak

print("=== Building HoodQuest On-Chain Cartridge (with Chunk 1-7 Invariance) ===")

with open('cache/original_payload.html', 'r', encoding='utf-8') as f:
    orig = f.read()

with open('prototype/index.html', 'r', encoding='utf-8') as f:
    current = f.read()

# Update pet flavor to remove false implication of on-chain bond modification
orig_mod = orig.replace('(+3 Bond Strengthened)', '(Camp Affection ❤️)')

pos_orig = orig_mod.find('// --- Loot Grid & Web3 Handlers ---')
pos_curr = current.find('// --- Loot Grid & Web3 Handlers ---')

if pos_orig == -1 or pos_curr == -1:
    raise ValueError("Split marker '// --- Loot Grid & Web3 Handlers ---' not found!")

new_payload = orig_mod[:pos_orig] + current[pos_curr:]

with open('prototype/hoodquest_cartridge_full.html', 'w', encoding='utf-8') as f:
    f.write(new_payload)

raw_bytes = new_payload.encode('utf-8')
comp_bytes = zlib.compress(raw_bytes, level=9)

CHUNK_SIZE = 24575
chunks = [comp_bytes[i:i+CHUNK_SIZE] for i in range(0, len(comp_bytes), CHUNK_SIZE)]

content_hash = "0x" + keccak.new(digest_bits=256).update(raw_bytes).hexdigest()
compressed_hash = "0x" + keccak.new(digest_bits=256).update(comp_bytes).hexdigest()

build_data = {
    "contentHash": content_hash,
    "compressedHash": compressed_hash,
    "uncompressedSize": len(raw_bytes),
    "compressedSize": len(comp_bytes),
    "chunks": ["0x" + c.hex() for c in chunks]
}

with open('cache/cartridge_build.json', 'w') as f:
    json.dump(build_data, f, indent=2)

print(f"Uncompressed Size: {len(raw_bytes):,} bytes")
print(f"Compressed Size:   {len(comp_bytes):,} bytes (Deflate level 9)")
print(f"Chunks ({len(chunks)}):")
for idx, c in enumerate(chunks):
    print(f"  Chunk {idx+1}: {len(c):,} bytes (limit: {CHUNK_SIZE})")
print(f"Content Hash:    {content_hash}")
print(f"Compressed Hash: {compressed_hash}")

# Verify Chunks 1-7 bit-for-bit against original deployed bytecode
orig_comp = zlib.compress(orig.encode('utf-8'), level=9)
for i in range(7):
    assert comp_bytes[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE] == orig_comp[i*CHUNK_SIZE:(i+1)*CHUNK_SIZE], f"Chunk {i+1} mismatch!"
print("Verification: Chunks 1-7 are 100% BIT-FOR-BIT IDENTICAL to on-chain deployed chunks!")

# Sanity verify decompression
decomp = zlib.decompress(b"".join(chunks))
assert decomp == raw_bytes, "Decompression verification failed!"
print("Decompression Verification: PASSED (100% exact match)")
