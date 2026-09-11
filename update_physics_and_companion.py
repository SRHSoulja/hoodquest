import re

with open('/home/arson/rhnftproject/prototype/simulator.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Day 0 Companion Fix
old_comp_start = """  function drawCompanion(c, info) {
    let petType = companionOverride !== 'auto' ? companionOverride : (c.companion || 'Camp Hound');
    if (petType === 'None') return;
    if (companionOverride === 'auto' && info.stageNum < 2) return;"""

new_comp_start = """  function drawCompanion(c, info) {
    let petType = companionOverride !== 'auto' ? companionOverride : (c.companion || 'None');
    if (petType === 'None' || !petType) return;"""

assert old_comp_start in text, "old_comp_start not found!"
text = text.replace(old_comp_start, new_comp_start)
print("Updated drawCompanion Day 0 rendering condition!")

# 2. Update updateAndDrawParticles to handle new types
old_parts = """      } else if (p.type === 'emerald') {
        ctx.fillStyle = `rgba(46, 204, 113, ${p.life * 0.85})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();"""

new_parts = """      } else if (p.type === 'emerald') {
        ctx.fillStyle = `rgba(46, 204, 113, ${p.life * 0.85})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      } else if (p.type === 'heart') {
        ctx.fillStyle = `rgba(239, 68, 68, ${p.life})`;
        ctx.font = `${p.size || 13}px sans-serif`;
        ctx.fillText('❤️', p.x, p.y);
      } else if (p.type === 'foam') {
        ctx.fillStyle = `rgba(255, 253, 240, ${p.life * 0.9})`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
      } else if (p.type === 'magic') {
        ctx.fillStyle = `rgba(168, 85, 247, ${p.life * 0.85})`;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
      } else if (p.type === 'wood_chip') {
        ctx.fillStyle = `rgba(139, 69, 19, ${p.life})`;
        ctx.fillRect(p.x, p.y, p.size, p.size * 1.5);
      } else if (p.type === 'musical_sparkle') {
        ctx.fillStyle = `rgba(255, 215, 0, ${p.life})`;
        ctx.font = 'bold 13px serif';
        ctx.fillText(p.symbol || '♫', p.x, p.y);
      }
      ctx.restore();"""

assert old_parts in text, "old_parts not found!"
text = text.replace(old_parts, new_parts)
print("Updated particle system types!")

# 3. Update drawTarget to render beer drips and soundwave rings
old_target = """    rings.forEach(ring => {
      ctx.fillStyle = ring.color;
      ctx.beginPath();
      ctx.arc(0, 0, ring.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#2b1b11';
      ctx.lineWidth = 1;
      ctx.stroke();
    });
    ctx.restore();"""

new_target = """    rings.forEach(ring => {
      ctx.fillStyle = ring.color;
      ctx.beginPath();
      ctx.arc(0, 0, ring.r, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#2b1b11';
      ctx.lineWidth = 1;
      ctx.stroke();
    });

    // Frothy ale drips down target face from tankard smash!
    if (t.beerDripTimer > 0) {
      t.beerDripTimer--;
      ctx.fillStyle = 'rgba(255, 253, 240, 0.88)';
      ctx.beginPath(); ctx.ellipse(0, -2, t.r * 0.45, t.r * 0.25, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(245, 180, 40, 0.7)';
      ctx.fillRect(-5, 0, 2.5, 14);
      ctx.fillRect(1, 2, 2.5, 18);
      ctx.fillRect(6, -1, 2.2, 10);
    }

    // Expanding golden harmonic soundwave rings from minstrel lute!
    if (t.soundwaveTimer > 0) {
      t.soundwaveTimer--;
      const waveR = (40 - t.soundwaveTimer) * 1.6;
      ctx.strokeStyle = `rgba(255, 215, 0, ${t.soundwaveTimer / 40})`;
      ctx.lineWidth = 2.2;
      ctx.beginPath(); ctx.arc(0, 0, waveR, 0, Math.PI * 2); ctx.stroke();
    }

    ctx.restore();"""

assert old_target in text, "old_target not found!"
text = text.replace(old_target, new_target)
print("Updated drawTarget!")

# 4. Update projectile impact physics
s_hit = text.find('// Exact collision detection with target face')
assert s_hit != -1
e_hit = text.find('} else if (a.y > 380 || a.x > W + 20) {', s_hit)
assert e_hit != -1

old_hit_block = text[s_hit:e_hit]

new_hit_block = """// Exact collision detection with target face
        if (dist <= tgt.r || (a.x >= tgt.x - 3 && a.vx > 0 && Math.abs(a.y - tgt.y) <= tgt.r)) {
          tgt.hits++;
          tgt.wobble = a.isGolden ? 32 : (a.type === 'oak_cudgel' ? 36 : 22);

          const isPiercing = (a.type === 'arrow' || a.type === 'stiletto' || a.type === 'duelist_blade' || a.type === 'iron_bolt');

          if (isPiercing) {
            a.stuck = true;
          } else if (a.type === 'oak_cudgel') {
            // Rebounds off target with heavy thud and wood splinters!
            a.vx = -4 - Math.random() * 2;
            a.vy = -3.5 - Math.random() * 2;
            a.gravity = 0.45;
            a.spinSpeed = 0.38;
            a.bouncing = true;
            a.bounceLife = 24;
            for (let k = 0; k < 10; k++) {
              particles.push({
                x: a.x, y: a.y,
                vx: (Math.random() - 0.5) * 3, vy: -Math.random() * 3,
                size: 2.2, type: 'wood_chip', life: 0.9, decay: 0.04
              });
            }
          } else if (a.type === 'ale_mug') {
            // Smashes into foam explosion! Target gets dripping ale trails!
            tgt.beerDripTimer = 75;
            for (let k = 0; k < 18; k++) {
              const ang = Math.random() * Math.PI * 2;
              const spd = 1.6 + Math.random() * 2.6;
              particles.push({
                x: a.x, y: a.y,
                vx: Math.cos(ang) * spd, vy: Math.sin(ang) * spd,
                size: 3.4, type: 'foam', life: 1.0, decay: 0.035
              });
            }
            arrows.splice(i, 1);
          } else if (a.type === 'potion') {
            // Shatters into vibrant alchemical mist!
            for (let k = 0; k < 22; k++) {
              const ang = Math.random() * Math.PI * 2;
              const spd = 1.8 + Math.random() * 3.0;
              particles.push({
                x: a.x, y: a.y,
                vx: Math.cos(ang) * spd, vy: Math.sin(ang) * spd,
                size: 3.2, type: 'magic', life: 1.2, decay: 0.03
              });
            }
            arrows.splice(i, 1);
          } else if (a.type === 'harmonic_note') {
            // Detonates into expanding soundwave rings!
            tgt.soundwaveTimer = 40;
            for (let k = 0; k < 10; k++) {
              particles.push({
                x: a.x + (Math.random() - 0.5) * 16, y: a.y + (Math.random() - 0.5) * 16,
                vx: (Math.random() - 0.5) * 1.5, vy: -1.2 - Math.random() * 1.5,
                size: 14, type: 'musical_sparkle', symbol: ['♪', '♫', '♬'][k % 3], life: 1.0, decay: 0.03
              });
            }
            arrows.splice(i, 1);
          } else if (a.type === 'acorn') {
            // Ricochets off target!
            a.vx = -4.5;
            a.vy = -3;
            a.gravity = 0.45;
            a.bouncing = true;
            a.bounceLife = 20;
          } else if (a.type === 'coin_pouch') {
            // Thuds and drops, spilling coins!
            a.vx = -1.8;
            a.vy = -1.2;
            a.gravity = 0.55;
            a.bouncing = true;
            a.bounceLife = 24;
            for (let k = 0; k < 14; k++) {
              particles.push({
                x: a.x, y: a.y,
                vx: (Math.random() - 0.5) * 3, vy: -1 - Math.random() * 2.5,
                size: 2.8, type: 'spark', life: 1.0, decay: 0.04
              });
            }
          }

          // Archetype-adaptive impact sound & toasts
          if (a.type === 'stiletto') {
            playSound(dist <= tgt.r * 0.38 ? 'bell' : 'hit');
            showToast(dist <= tgt.r * 0.38 ? '🗡️🎯 MAID MARIAN STILETTO BULLSEYE! 🔔' : '🗡️ Maid Marian\\'s Stiletto Struck the Target!');
          } else if (a.type === 'oak_cudgel') {
            playSound('hit');
            showToast('🪵 Little John\\'s Oak Cudgel Struck with Mountain Force!');
          } else if (a.type === 'ale_mug') {
            playSound('purr');
            showToast('🍺 Friar Tuck\\'s Foaming Ale Splashed the Mark!');
          } else if (a.type === 'potion') {
            playSound('fire');
            showToast('🧪 Mother Meg\\'s Mystic Elixir Engulfed the Target in Vapor!');
          } else if (a.type === 'harmonic_note') {
            playSound('lute');
            showToast('🎵 Alan-a-Dale\\'s Harmonic Note Resonates Across the Forest!');
          } else if (a.type === 'duelist_blade') {
            playSound('hit');
            showToast('⚔️ Will Scarlet\\'s Duelist Blade Struck Clean!');
          } else if (a.type === 'acorn') {
            playSound('munch');
            showToast('🌰 Much\\'s Slingshot Acorn Nailed the Mark!');
          } else if (a.type === 'iron_bolt') {
            playSound('hit');
            showToast('🛡️ Guy of Gisborne\\'s Heavy Cross-Bolt Pierced the Wood!');
          } else if (a.type === 'coin_pouch') {
            playSound('bell');
            showToast('💰 The Sheriff\\'s Heavy Tax Purse Smacked the Target with a Clink!');
          } else { // arrow
            if (dist <= tgt.r * 0.38) {
              playSound('bell');
              showToast(a.isGolden ? '✨👑 MYTHIC GOLDEN ARROW BULLSEYE! 🎯🔔' : '🎯 DEAD CENTER BULLSEYE! 🔔');
            } else {
              playSound('hit');
              showToast(a.isGolden ? '✨ Golden Arrow Struck Target!' : '🎯 Target Hit!');
            }
          }
        """

text = text[:s_hit] + new_hit_block + text[e_hit:]
print("Updated projectile collision impact logic!")

# 5. Handle bouncing projectiles fadeout
s_stick_check = text.find('} else if (a.y > 380 || a.x > W + 20) {')
assert s_stick_check != -1
old_stick_clause = """        } else if (a.y > 380 || a.x > W + 20) {
          a.stuck = true;
        }"""
new_stick_clause = """        } else if (a.y > 380 || a.x > W + 20) {
          if (a.bouncing) {
            arrows.splice(i, 1);
            continue;
          } else {
            a.stuck = true;
          }
        }
        if (a.bouncing) {
          a.bounceLife--;
          if (a.bounceLife <= 0) {
            arrows.splice(i, 1);
            continue;
          }
        }"""
assert old_stick_clause in text, "old_stick_clause not found!"
text = text.replace(old_stick_clause, new_stick_clause)
print("Updated bouncing projectile cleanup!")

# 6. Canvas Click Petting Handler (No invisible pets!)
old_pet_click = """    } else if (Math.hypot(clickX - 240, clickY - 360) < 25) { // Click pet
      initAudio();
      playSound('purr');
      showToast(`🐾 Petted ${currentToken.companion}!`);
    }"""

new_pet_click = """    } else if (Math.hypot(clickX - 240, clickY - 360) < 32) { // Click pet
      const activePet = companionOverride !== 'auto' ? companionOverride : (currentToken ? currentToken.companion : 'None');
      if (activePet === 'None' || !activePet) {
        showToast('🐾 No companion in camp! Bond with a beast at Mother Meg\\'s Sanctuary.');
      } else {
        petAnim.petTimer = 25;
        for (let k = 0; k < 6; k++) {
          particles.push({
            x: 240 + (Math.random() - 0.5) * 16,
            y: 355 + (Math.random() - 0.5) * 12,
            vx: (Math.random() - 0.5) * 0.8,
            vy: -1.2 - Math.random() * 1.2,
            size: 14,
            type: 'heart',
            life: 1.0,
            decay: 0.04
          });
        }
        initAudio();
        playSound('purr');
        showToast(`🐾 Petted ${activePet}! (+3 Bond Strengthened)`);
      }
    }"""

assert old_pet_click in text, "old_pet_click not found!"
text = text.replace(old_pet_click, new_pet_click)
print("Updated canvas pet clicking handler!")

# 7. Check if drawTarget should check backdropProps.target in loop()
s_loop = text.find('function loop() {')
assert s_loop != -1
old_draw_tgt = "drawTarget();"
new_draw_tgt = "if (backdropProps.target) drawTarget();"
text = text[:s_loop] + text[s_loop:].replace(old_draw_tgt, new_draw_tgt, 1)
print("Updated loop to respect backdropProps.target!")

with open('/home/arson/rhnftproject/prototype/simulator.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("All simulator physics & companion updates applied successfully!")
