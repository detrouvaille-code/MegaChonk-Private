import * as THREE from "three";
import { clone } from "three/addons/utils/SkeletonUtils.js";
import { ORANGE_CAT_RESCUE } from "./adventure-rules.js";

function orangeCat(source) {
  const model = clone(source);
  model.name = "RescuedOrangeCatRig";
  const accessories = [];
  model.traverse((object) => {
    if (!object.isMesh) return;
    if (["EquippedCollar", "EquippedPendant"].includes(object.name)) { accessories.push(object); return; }
    // Own these resources so clearing the cage never disposes the playable cat.
    object.geometry = object.geometry.clone();
    const materials = (Array.isArray(object.material) ? object.material : [object.material]).map((material) => {
      const copy = material.clone();
      if (copy.map) copy.map = copy.map.clone();
      return copy;
    });
    object.material = Array.isArray(object.material) ? materials : materials[0];
    if (object.morphTargetInfluences) object.morphTargetInfluences.fill(0);
    if (!materials.some((material) => material.name === "TurkishVan.Fur")) return;
    const positions = object.geometry.attributes.position;
    const colors = new Float32Array(positions.count * 3);
    const ginger = new THREE.Color(0xd98638), stripe = new THREE.Color(0xa34c20), cream = new THREE.Color(0xf3d7a9);
    for (let index = 0; index < positions.count; index++) {
      const x = positions.getX(index), y = positions.getY(index), z = positions.getZ(index);
      const band = Math.sin(z * 33 + Math.sin(y * 14) * 1.4) > 0.72;
      const color = y < 0.095 ? cream : band && Math.abs(x) > 0.075 ? stripe : ginger;
      color.toArray(colors, index * 3);
    }
    object.geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
  });
  accessories.forEach((object) => object.removeFromParent());
  return model;
}

export class RescueMission {
  constructor({ root, progress, collider, surface, sign, source, onRescue }) {
    Object.assign(this, { root, progress, collider, surface, sign, source, onRescue });
    this.clear();
  }
  clear() {
    if (this.mixer) { this.mixer.stopAllAction(); this.mixer.uncacheRoot(this.cat); }
    const skeletons = new Set();
    this.cat?.traverse((object) => { if (object.isSkinnedMesh) skeletons.add(object.skeleton); });
    skeletons.forEach((skeleton) => skeleton.dispose());
    this.group = this.cat = this.mixer = null;
    this.idle = this.walk = this.gate = this.gateCollider = this.lock = null;
    this.openTime = 0;
  }
  build() {
    const [x, z] = ORANGE_CAT_RESCUE.cage;
    this.group = new THREE.Group();
    this.group.name = "OrangeCatRescue";
    this.group.userData.ownsMaterials = true;
    this.group.position.set(x, 0, z);
    this.root.add(this.group);
    const metal = new THREE.MeshStandardMaterial({ color: 0x536b6b, metalness: 0.65, roughness: 0.38 });
    const brass = new THREE.MeshStandardMaterial({ color: 0xd8ad61, metalness: 0.55, roughness: 0.4 });
    const cushion = new THREE.MeshStandardMaterial({ color: 0x6a8e78, roughness: 0.95 });
    const box = (parent, name, size, position, material = metal) => {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(...size), material);
      mesh.name = name;
      mesh.position.set(...position);
      mesh.castShadow = mesh.receiveShadow = true;
      parent.add(mesh);
      return mesh;
    };
    box(this.group, "CageBase", [3.5, 0.12, 2.7], [0, 0.06, 0]);
    box(this.group, "RescueCushion", [2.9, 0.05, 2.2], [0, 0.145, 0], cushion);
    this.gate = new THREE.Group();
    this.gate.name = "RescueCageGate";
    this.group.add(this.gate);
    for (const side of [-1, 1]) {
      for (let offset = -1.25; offset <= 1.26; offset += 0.31) box(this.group, "CageSideBar", [0.055, 1.9, 0.055], [side * 1.7, 1.05, offset]);
      for (const y of [0.2, 2.0]) box(this.group, "CageSideRail", [0.085, 0.085, 2.7], [side * 1.7, y, 0]);
    }
    for (let offset = -1.65; offset <= 1.66; offset += 0.3) {
      box(this.group, "CageBackBar", [0.055, 1.9, 0.055], [offset, 1.05, -1.3]);
      box(this.gate, "CageFrontBar", [0.055, 1.9, 0.055], [offset, 1.05, 1.3]);
      box(this.group, "CageRoofBar", [0.055, 0.055, 2.7], [offset, 2.0, 0]);
    }
    for (const y of [0.2, 2.0]) {
      box(this.group, "CageBackRail", [3.5, 0.085, 0.085], [0, y, -1.3]);
      box(this.gate, "CageFrontRail", [3.5, 0.085, 0.085], [0, y, 1.3]);
    }
    this.lock = box(this.gate, "CageLock", [0.22, 0.27, 0.12], [0, 0.9, 1.36], brass);
    const baseCollider = this.collider(x, z, 3.5, 2.7, 0, 0, 0.12, this.group);
    baseCollider.stepUp = true;
    this.surface(x, z, 3.5, 2.7, 0.12, this.group).inset = 0;
    this.collider(x, z, 3.5, 2.7, 0, 1.97, 2.06, this.group);
    for (const side of [-1, 1]) this.collider(x + side * 1.7, z, 0.085, 2.7, 0, 0.12, 2.05, this.group);
    this.collider(x, z - 1.3, 3.5, 0.085, 0, 0.12, 2.05, this.group);
    this.gateCollider = this.collider(x, z + 1.3, 3.5, 0.085, 0, 0.12, 2.05, this.gate);
    this.sign("ORANGE CAT RESCUE", x, 3.1, z + 1.3, "#f4bd75");
    this.sign("3 MICE / 2 SWIPES EACH", x, 2.5, z + 1.3, "#f4bd75");
    const { model, idle, walk } = this.source();
    this.cat = orangeCat(model);
    this.cat.position.set(0, 0.17, -0.15);
    this.cat.rotation.y = 0;
    this.group.add(this.cat);
    this.mixer = new THREE.AnimationMixer(this.cat);
    this.idle = this.mixer.clipAction(idle);
    this.walk = this.mixer.clipAction(walk);
    this.idle.play();
    if (this.progress.orangeCatRescued) {
      this.openTime = 5;
      this.gate.position.y = 2.2;
      this.cat.position.z = 2.5;
      this.cat.position.y = 0;
      this.gateCollider.enabled = false;
      this.lock.visible = false;
    }
  }
  update(delta, active) {
    if (!this.group || !active) return;
    this.mixer.update(delta);
    if (this.progress.guardsRemaining > 0 || this.progress.orangeCatRescued) return;
    this.openTime += delta;
    this.gate.position.y = Math.min(2.2, this.openTime * 1.8);
    this.gateCollider.minY = 0.12 + this.gate.position.y;
    this.gateCollider.maxY = 2.05 + this.gate.position.y;
    this.lock.visible = false;
    if (this.openTime > 1.3) {
      if (!this.walk.isRunning()) { this.idle.fadeOut(0.2); this.walk.reset().fadeIn(0.2).play(); }
      this.cat.position.z = Math.min(2.5, -0.15 + (this.openTime - 1.3) * 1.1);
      this.cat.position.y = 0.17 * (1 - THREE.MathUtils.smoothstep(this.cat.position.z, 1.1, 1.9));
      if (this.cat.position.z >= 2.5 && this.progress.rescueCat()) {
        this.walk.fadeOut(0.2);
        this.idle.reset().fadeIn(0.2).play();
        this.onRescue();
      }
    }
  }
  get protectedAreas() { return this.group ? [{ minX: -7.5, maxX: 7.5, minZ: -18.1, maxZ: -10.8 }] : []; }
  get targets() { return this.group ? ORANGE_CAT_RESCUE.guards.map(({ x, z }) => [x, 0, z + 3.2]) : []; }
  snapshot() {
    return this.group ? { active: true, freed: this.progress.orangeCatRescued, guardsRemaining: this.progress.guardsRemaining, cage: [...ORANGE_CAT_RESCUE.cage], targets: this.targets, gateLift: this.gate.position.y, catPosition: this.cat.getWorldPosition(new THREE.Vector3()).toArray(), skinned: true } : null;
  }
}
