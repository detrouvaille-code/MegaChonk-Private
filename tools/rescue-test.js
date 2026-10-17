const assert = require("assert/strict");
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const path = require("path");
const capture = require("./capture-screenshot");
const root = path.resolve(__dirname, "..");

(async () => {
  const server = spawn("python", ["-m", "http.server", "4183", "--bind", "127.0.0.1"], { cwd: root, stdio: "ignore", windowsHide: true });
  let browser;
  const errors = [], results = [];
  try {
    browser = await chromium.launch({ headless: true, executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" });
    for (const mobile of [false, true]) {
      const context = await browser.newContext(mobile ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1440, height: 900 } });
      const page = await context.newPage();
      page.on("pageerror", (error) => errors.push(error.message));
      page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); });
      await page.goto("http://127.0.0.1:4183", { waitUntil: "networkidle" });
      await page.waitForFunction(() => window.__megaChonk?.state.ready, null, { timeout: 60000 });
      await page.evaluate(() => window.__megaChonk.start());
      await page.waitForFunction(() => !window.__megaChonk.state.transitioning);
      await page.evaluate(() => { window.__megaChonk.regenerate(424242); window.__megaChonk.loadLevel(1); });
      const snap = () => page.evaluate(() => ({ ...window.__megaChonk.snapshot(), goal: window.__megaChonk.navigation().goal }));
      const place = (x, z, heading = 0) => page.evaluate(({ x, z, heading }) => {
        const g = window.__megaChonk;
        g.character.root.position.set(x, 0, z);
        g.character.velocity.set(0, 0, 0);
        g.character.verticalVelocity = 0;
        g.character.heading = heading;
        g.character.root.rotation.y = heading;
        Object.assign(g.state, { grounded: true, forcedAction: null, actionTime: 0, sitting: false, invulnerable: 10 });
      }, { x, z, heading });
      const attack = async (kind = "claw") => {
        await page.waitForFunction(() => window.__megaChonk.state.attackCooldown === 0);
        if (mobile) await page.tap(`[data-touch-action="${kind}"]`);
        else await page.keyboard.press(kind === "claw" ? "f" : "e");
        await page.waitForFunction(() => !window.__megaChonk.state.pendingAttack);
      };
      let s = await snap();
      assert.equal(s.foodsRemaining, 0);
      assert.equal(s.goal.active, false);
      assert.equal(s.rescue.guardsRemaining, 3);
      assert.ok(s.adventure.enemies.every((enemy) => enemy.guard && enemy.health === 2));
      if (mobile) {
        for (const size of [{ width: 320, height: 568 }, { width: 568, height: 320 }, { width: 844, height: 390 }, { width: 390, height: 844 }]) {
          await page.setViewportSize(size);
          await page.waitForTimeout(100);
          const panels = await page.evaluate(() => [".objective-panel", ".ability-panel", ".status-panel"].map((selector) => {
            const box = document.querySelector(selector).getBoundingClientRect();
            return { selector, x: box.x, y: box.y, right: box.right, bottom: box.bottom };
          }));
          for (const panel of panels) assert.ok(panel.x >= 0 && panel.y >= 0 && panel.right <= size.width + 1 && panel.bottom <= size.height + 1, `Rescue HUD is offscreen at ${size.width}x${size.height}`);
          for (const [index, a] of panels.entries()) for (const b of panels.slice(index + 1)) assert.ok(!(a.x < b.right && a.right > b.x && a.y < b.bottom && a.bottom > b.y), `Rescue HUD overlaps: ${a.selector}/${b.selector}`);
        }
      }
      assert.equal(await page.evaluate(() => {
        const g = window.__megaChonk;
        const npc = g.character.root.parent.getObjectByName("RescuedOrangeCatRig");
        let source;
        g.character.model.traverse((object) => { if (object.isSkinnedMesh && object.material.name === "TurkishVan.Fur" && (!source || object.geometry.attributes.position.count > source.geometry.attributes.position.count)) source = object; });
        const copy = npc.getObjectByName(source.name);
        return copy.isSkinnedMesh && source.geometry !== copy.geometry && source.material !== copy.material && source.skeleton !== copy.skeleton && copy.geometry.attributes.color.getX(100) !== source.geometry.attributes.color.getX(100);
      }), true, "The orange NPC must be a separate skinned cat with its own orange coat");
      if (!mobile) {
        await place(0, -14, Math.PI);
        await page.evaluate(() => { window.__megaChonk.state.yaw = 0; });
        await page.keyboard.down("w"); await page.waitForTimeout(650); await page.keyboard.up("w");
        assert.ok((await snap()).position[2] > -14.6, "The locked cage must physically block entry");
        await place(0, -18.4);
        await page.waitForTimeout(250);
        assert.equal((await snap()).level, 1, "Walking to the exit cannot skip the rescue");
        await place(2.8, -12.5, Math.PI);
        await page.evaluate(() => { const s = window.__megaChonk.state; s.started = false; s.yaw = 0.45; s.pitch = 0.08; });
        await page.waitForTimeout(900);
        await capture(page, { path: path.join(root, "assets/previews/mega-chonk-orange-cat-rescue.png") });
        await page.evaluate(() => { window.__megaChonk.state.started = true; });
        const charm = (await snap()).adventure.items.find((item) => item.kind === "charm");
        await place(charm.x, charm.z);
        await page.waitForFunction(() => window.__megaChonk.adventureSnapshot().stats.clawDamage === 2);
      }
      const guards = (await snap()).adventure.enemies;
      for (let index = 0; index < guards.length; index++) {
        let enemy = (await snap()).adventure.enemies.find((enemy) => enemy.id === guards[index].id);
        await place(enemy.x, enemy.z - 1);
        await attack("bite");
        assert.equal((await snap()).adventure.enemies.find((candidate) => candidate.id === enemy.id).health, 2, "Bites cannot substitute for swipes");
        enemy = (await snap()).adventure.enemies.find((candidate) => candidate.id === enemy.id);
        await place(enemy.x, enemy.z - 1);
        await attack();
        assert.equal((await snap()).adventure.enemies.find((candidate) => candidate.id === enemy.id).health, 1);
        assert.equal((await snap()).goal.active, false);
        if (index === 0 && !mobile) {
          await page.evaluate(() => window.__megaChonk.regenerate(424242));
          assert.equal((await snap()).adventure.enemies.find((candidate) => candidate.id === enemy.id).health, 1, "Regeneration preserves partial guard progress");
        }
        enemy = (await snap()).adventure.enemies.find((candidate) => candidate.id === enemy.id);
        await place(enemy.x, enemy.z - 1);
        await attack();
        assert.equal((await snap()).adventure.enemies.find((candidate) => candidate.id === enemy.id).active, false);
        if (index < 2) {
          assert.equal((await snap()).rescue.gateLift, 0);
          assert.equal((await snap()).goal.active, false);
        }
      }
      await place(3.0, -14);
      await page.waitForFunction(() => window.__megaChonk.snapshot().rescue.freed && window.__megaChonk.navigation().goal.active, null, { timeout: 20000 });
      s = await snap();
      assert.equal(s.xp, 100);
      assert.equal(s.rescue.guardsRemaining, 0);
      assert.equal(s.rescue.gateLift, 2.2);
      assert.ok(s.rescue.catPosition[2] > -14);
      assert.ok(Math.abs(s.rescue.catPosition[1]) < 0.01, "The freed orange cat must stand on the house floor");
      await capture(page, { path: path.join(root, mobile ? "assets/previews/mega-chonk-orange-rescue-mobile.png" : "assets/previews/mega-chonk-orange-cat-freed.png") });
      if (!mobile) {
        await place(0, -14, Math.PI);
        await page.evaluate(() => { window.__megaChonk.state.yaw = 0; });
        await page.keyboard.down("w");
        await page.waitForFunction(() => window.__megaChonk.character.root.position.z < -15.5, null, { timeout: 5000 });
        await page.keyboard.up("w");
        await page.waitForFunction(() => window.__megaChonk.state.grounded);
        assert.ok((await snap()).position[1] >= 0.1, "The open cage must be enterable with a solid floor");
      }
      await page.evaluate(() => window.__megaChonk.regenerate(424242));
      assert.equal((await snap()).xp, 100, "Rebuilding must not award rescue XP twice");
      assert.equal((await snap()).rescue.freed, true);
      await place(0, -18.4);
      await page.waitForFunction(() => window.__megaChonk.state.level === 2, null, { timeout: 7000 });
      await page.evaluate(() => { window.__megaChonk.restart(); window.__megaChonk.loadLevel(1); });
      assert.equal((await snap()).rescue.freed, false);
      assert.equal((await snap()).rescue.guardsRemaining, 3);
      results.push({ mode: mobile ? "touch" : "keyboard", guards: 3, swipesPerGuard: 2, cageCollision: !mobile, exitUnlocked: true, reset: true });
      await context.close();
    }
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({ seed: 424242, results, errors }, null, 2));
    console.log("Orange-cat rescue integration passed");
  } finally { await browser?.close(); server.kill(); }
})().catch((error) => { console.error(error); process.exitCode = 1; });
