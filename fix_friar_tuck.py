import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure presets #1-#10 don't trigger isBeggar on default view
# Only trigger isBeggar if seed > 100 or specific disguise mode
old_gen = """    // Folklore Paper-Doll Variants: Beggar disguise & Change Cup!
    const isBeggar = (arch.id === 'friar' || arch.id === 'archer') && ((seed % 3) === 0);"""

new_gen = """    // Folklore Paper-Doll Variants: Beggar disguise & Change Cup (for seeds >= 100)
    const isBeggar = (arch.id === 'friar' || arch.id === 'archer') && (seed >= 100 && (seed % 3) === 0);"""

assert old_gen in text, "old_gen not found!"
text = text.replace(old_gen, new_gen)
print("Updated isBeggar condition!")

# Now replace the Friar Tuck drawing routine in drawCharacter
s_friar = text.find("} else if (archId === 'friar') {")
assert s_friar != -1
e_friar = text.find("} else if (archId === 'brawler') {", s_friar)
assert e_friar != -1

new_friar_block = """} else if (archId === 'friar') {
        // ==========================================
        // --- FRIAR TUCK (MASTERPIECE ARTISAN) ---
        // ==========================================
        // 1. Shaved Bald Tonsure Crown (Seamless with skull)
        ctx.fillStyle = skinBase;
        ctx.beginPath();
        ctx.ellipse(0, -73, 6.2, 4.0, 0, 0, Math.PI * 2);
        ctx.fill();

        // Soft healthy scalp highlight
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.beginPath();
        ctx.ellipse(1.5, -74, 3, 1.8, 0.2, 0, Math.PI * 2);
        ctx.fill();

        // 2. Curled Tonsure Fringe Ring (Hugs the skull from ear to ear!)
        ctx.fillStyle = hairSh;
        // Left hair temple & ear locks
        ctx.beginPath();
        ctx.moveTo(-5.5, -73.5);
        ctx.quadraticCurveTo(-9.5, -72, -9.8, -66);
        ctx.quadraticCurveTo(-10.5, -60, -7.5, -59);
        ctx.lineTo(-5.2, -61);
        ctx.quadraticCurveTo(-8.2, -65, -5.5, -73.5);
        ctx.closePath();
        ctx.fill();

        // Right hair temple & ear locks
        ctx.beginPath();
        ctx.moveTo(5.5, -73.5);
        ctx.quadraticCurveTo(9.5, -72, 9.8, -66);
        ctx.quadraticCurveTo(10.5, -60, 7.5, -59);
        ctx.lineTo(5.2, -61);
        ctx.quadraticCurveTo(8.2, -65, 5.5, -73.5);
        ctx.closePath();
        ctx.fill();

        // Continuous back tonsure hair mass connecting ears
        ctx.fillStyle = hairHex;
        ctx.beginPath();
        ctx.arc(0, -72, 9.0, -Math.PI * 0.96, -Math.PI * 0.04);
        ctx.lineTo(8.5, -66);
        ctx.quadraticCurveTo(0, -70, -8.5, -66);
        ctx.closePath();
        ctx.fill();

        // Textured curly strand tufts
        ctx.fillStyle = hairHex;
        ctx.beginPath();
        ctx.arc(-8.5, -66, 2.6, 0, Math.PI * 2);
        ctx.arc(-7.5, -61, 2.2, 0, Math.PI * 2);
        ctx.arc(8.5, -66, 2.6, 0, Math.PI * 2);
        ctx.arc(7.5, -61, 2.2, 0, Math.PI * 2);
        ctx.fill();

        // Highlights on curls
        ctx.strokeStyle = hairHi;
        ctx.lineWidth = 1.1;
        ctx.beginPath();
        ctx.arc(-8.5, -66, 2.6, -Math.PI * 0.5, Math.PI * 0.5);
        ctx.arc(8.5, -66, 2.6, Math.PI * 0.5, -Math.PI * 0.5);
        ctx.stroke();

        // 3. Monastic Habit Cowl (Wool collar draped over shoulders)
        ctx.fillStyle = '#3a2110';
        ctx.beginPath();
        ctx.moveTo(-11, -54);
        ctx.quadraticCurveTo(0, -47, 11, -54);
        ctx.lineTo(8, -61);
        ctx.quadraticCurveTo(0, -56, -8, -61);
        ctx.closePath();
        ctx.fill();

        // Cowl fold shadow
        ctx.strokeStyle = '#261407';
        ctx.lineWidth = 1.2;
        ctx.beginPath();
        ctx.moveTo(-9, -56);
        ctx.quadraticCurveTo(0, -50, 9, -56);
        ctx.stroke();

        // 4. Carved Oak Ale Tankard (Grip in hand)
        const mugX = isActing ? 12 : 9;
        const mugY = isActing ? -64 : -50;
        ctx.fillStyle = '#6b4323';
        ctx.beginPath();
        ctx.roundRect(mugX, mugY, 14, 17, 2);
        ctx.fill();
        // Wrought iron hoops
        ctx.fillStyle = '#475569';
        ctx.fillRect(mugX, mugY + 3, 14, 2);
        ctx.fillRect(mugX, mugY + 12, 14, 2);
        // Mug handle
        ctx.strokeStyle = '#4a2a12';
        ctx.lineWidth = 2.2;
        ctx.strokeRect(mugX + 13, mugY + 4, 4, 9);
        // Creamy frothing foam head
        ctx.fillStyle = '#fffdf0';
        ctx.beginPath();
        ctx.ellipse(mugX + 7, mugY - 1, 8.5, 4.5, 0, 0, Math.PI * 2);
        ctx.fill();
        // Foaming bubbles
        ctx.beginPath();
        ctx.arc(mugX + 3, mugY + 4, 1.4, 0, Math.PI * 2);
        ctx.arc(mugX + 10, mugY + 6, 1.2, 0, Math.PI * 2);
        ctx.fill();

        // Hand holding tankard handle
        ctx.fillStyle = skinBase;
        ctx.beginPath();
        ctx.arc(mugX + 14, mugY + 8, 3.2, 0, Math.PI * 2);
        ctx.fill();

      """

text = text[:s_friar] + new_friar_block + text[e_friar:]
print("Updated Friar Tuck masterpiece block!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
