const assert = require("assert/strict");
const { chromium } = require("playwright");
const { spawn } = require("child_process");
const path = require("path");
const capture = require("./capture-screenshot");
const root = path.resolve(__dirname, "..");

(async () => {
  const target = process.argv[2] || "http://127.0.0.1:4185/";
  const server = process.argv[2] ? null : spawn("python", ["-m", "http.server", "4185", "--bind", "127.0.0.1"], { cwd: root, stdio: "ignore", windowsHide: true });
  let browser;
  const errors = [];
  try {
    browser = await chromium.launch({ headless: true, executablePath: "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" });
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    page.on("pageerror", error => errors.push(error.message));
    page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
    await page.goto(target, { waitUntil: "networkidle" });
    await page.waitForFunction(() => window.__megaChonk?.state.ready);
    const select = async (id) => {
      await page.selectOption("#character-select", id);
      await page.waitForFunction(id => window.__megaChonk.state.ready && window.__megaChonk.character.id === id, id);
    };
    assert.equal(await page.evaluate(() => __megaChonk.character.id), "van");
    for (const id of ["tactical-tabby", "van", "tactical-tabby"]) await select(id);
    await page.reload({ waitUntil: "networkidle" });
    await page.waitForFunction(() => window.__megaChonk?.state.ready);
    assert.equal(await page.evaluate(() => __megaChonk.character.id), "tactical-tabby", "Remember the player's choice");
    const bootLayouts = [];
    for (const [width, height] of [[320, 568], [568, 320], [390, 844], [844, 390]]) {
      await page.setViewportSize({ width, height });
      const fit = await page.evaluate(() => {
        const select = document.querySelector("#character-select").getBoundingClientRect();
        const enter = document.querySelector("#enter-game").getBoundingClientRect();
        const credits = document.querySelector(".boot-credits").getBoundingClientRect();
        return { selectTop: select.top, enterBottom: enter.bottom, creditsBottom: credits.bottom, overflow: document.documentElement.scrollWidth > innerWidth };
      });
      assert.ok(fit.selectTop >= 0 && fit.creditsBottom <= height - 30 && !fit.overflow, `Boot fits ${width}x${height}: ${JSON.stringify(fit)}`);
      bootLayouts.push({ width, height, ...fit });
    }
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.click("#enter-game");
    await page.waitForFunction(() => !__megaChonk.state.transitioning);
    assert.equal(await page.locator("#character-select").isDisabled(), true);
    const snapshot = () => page.evaluate(() => __megaChonk.snapshot());
    assert.equal((await snapshot()).modelName, "TacticalTabbySkinnedRig");
    assert.equal((await snapshot()).animationClips, 7);
    const coat = await page.evaluate(() => {
      const surface = [], strands = [];
      __megaChonk.character.model.traverse(mesh => {
        if (!mesh.isSkinnedMesh) return;
        const material = mesh.material;
        const record = { name: mesh.name, uv: Boolean(mesh.geometry.attributes.uv), colors: Boolean(mesh.geometry.attributes.color), map: material.map?.image?.width || 0, normal: material.normalMap?.image?.width || 0, alphaTest: material.alphaTest, doubleSided: material.side === 2 };
        if (material.name === "TacticalTabby.Fur.GroomedSurface") surface.push(record);
        if (material.name === "TacticalTabby.Fur.GroomedStrands") strands.push(record);
      });
      return { surface, strands };
    });
    assert.ok(coat.surface.length >= 10 && coat.surface.every(m => m.uv && m.colors && m.map >= 512 && m.normal >= 512), "Skin keeps its UV-mapped coat and directional normal map in the game");
    assert.ok(coat.strands.length >= 10 && coat.strands.every(m => m.uv && m.colors && m.map >= 1024 && m.alphaTest > .3 && m.doubleSided), "Fur cards retain the embedded strand atlas, alpha mask and double-sided rendering");
    const timing = await page.evaluate(() => new Promise(resolve => {
      const samples=[];let last;
      const frame=time=>{if(last) samples.push(time-last);last=time;if(samples.length<90)requestAnimationFrame(frame);else{samples.sort((a,b)=>a-b);resolve({medianFPS:1000/samples[45],p95FrameMs:samples[85]});}};
      requestAnimationFrame(frame);
    }));
    await page.evaluate(() => { __megaChonk.state.yaw = 0; });
    const before = (await snapshot()).position[2];
    await page.keyboard.down("w"); await page.waitForTimeout(650); await page.keyboard.up("w");
    assert.ok((await snapshot()).position[2] < before - .5);
    await page.keyboard.press("Space");
    await page.waitForFunction(() => !__megaChonk.state.grounded);
    await page.waitForFunction(() => __megaChonk.state.grounded);
    for (const [key, action] of [["q", "Sit"], ["f", "Claw"], ["e", "Bite"]]) {
      await page.waitForFunction(() => !__megaChonk.state.forcedAction && __megaChonk.state.attackCooldown <= 0);
      await page.keyboard.press(key);
      try {
        await page.waitForFunction(action => __megaChonk.snapshot().activeAnimation?.startsWith(action), action);
      } catch (error) {
        throw new Error(`${action} did not start: ${JSON.stringify(await snapshot())}`, { cause: error });
      }
      if (action !== "Sit") await page.waitForFunction(() => !__megaChonk.state.forcedAction && __megaChonk.state.attackCooldown <= 0);
    }
    await page.evaluate(() => { __megaChonk.state.started = false; __megaChonk.state.forcedAction = null; });
    const poses = [];
    for (const action of ["Idle", "Walk", "Sit", "Groom", "Jump", "Claw", "Bite"]) {
      for (const fraction of [.05, .25, .5, .75, .95]) {
        const bounds = await page.evaluate(async ({ action, fraction }) => {
          const THREE = await import(new URL("vendor/three/build/three.module.js", location.href).href);
          const { character: c, state: s } = __megaChonk;
          c.mixer.stopAllAction();
          const a = c.actions[action]; a.reset().setEffectiveWeight(1).play(); a.time = a.getClip().duration * fraction; a.paused = true;
          c.currentAction = a; c.mixer.update(0); c.model.updateMatrixWorld(true);
          let min = Infinity, max = -Infinity, finite = true;
          const p = new THREE.Vector3();
          c.model.traverse(mesh => {
            if (!mesh.isSkinnedMesh) return;
            mesh.skeleton.update();
            for (let i = 0; i < mesh.geometry.attributes.position.count; i += 13) {
              mesh.getVertexPosition(i, p).applyMatrix4(mesh.matrixWorld);
              min = Math.min(min, p.y - c.root.position.y); max = Math.max(max, p.y - c.root.position.y);
              finite &&= [p.x, p.y, p.z].every(Number.isFinite);
            }
          });
          return { min, max, finite };
        }, { action, fraction });
        assert.ok(bounds.finite && bounds.max < 1.3, `${action} finite bounds`);
        if (["Idle", "Walk", "Sit", "Groom"].includes(action)) assert.ok(bounds.min > -.025, `${action} floor contact: ${JSON.stringify(bounds)}`);
        poses.push({ action, fraction, ...bounds });
      }
    }
    await page.evaluate(() => { __megaChonk.character.mixer.stopAllAction(); const a = __megaChonk.character.actions.Idle; a.reset().play(); a.paused = true; __megaChonk.character.currentAction = a; __megaChonk.state.yaw = Math.PI; __megaChonk.setCondition(60, 100); });
    await page.waitForFunction(() => __megaChonk.snapshot().bodyMorph.influence > .9);
    assert.ok((await snapshot()).bodyMorph.meshes > 1, "Clothing and body have a chonk morph");
    await page.evaluate(() => __megaChonk.setCondition(60, 40));
    await page.waitForFunction(() => __megaChonk.snapshot().bodyMorph.influence < .02);
    await capture(page, { path: path.join(root, "assets/previews/mega-chonk-tactical-tabby.png") });
    await page.evaluate(() => __megaChonk.loadLevel(1));
    const npc = await page.evaluate(() => {
      const player = __megaChonk.character.model;
      const npc = player.parent.parent.getObjectByName("RescuedOrangeCatRig");
      let hasVan = false, hasGear = false;
      npc.traverse(obj => {
        if (/TacticalTabby|Headset|Radio/.test(obj.name)) hasGear = true;
        if (obj.isMesh && (Array.isArray(obj.material) ? obj.material : [obj.material]).some(m => m.name === "TurkishVan.Fur")) hasVan = true;
      });
      return { hasVan, hasGear, guards: __megaChonk.snapshot().adventure.enemies.filter(e => e.guard).length };
    });
    assert.deepEqual(npc, { hasVan: true, hasGear: false, guards: 3 });
    assert.deepEqual(errors, []);
    console.log(JSON.stringify({ character: (await snapshot()).characterName, coat, timing, bootLayouts, poses, npc, errors }, null, 2));
    console.log("Tactical character integration passed");
  } finally {
    if (browser) await browser.close();
    server?.kill();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
