import * as THREE from "three";

function catFace(context, x, y, scale = 1, engraved = false) {
  context.save();
  context.translate(x, y);
  context.scale(scale, scale);
  context.lineWidth = 4;
  context.lineJoin = "round";
  context.lineCap = "round";
  context.strokeStyle = "#233e40";
  context.fillStyle = engraved ? "#9caeaf" : "#fff9e9";
  context.beginPath();
  context.moveTo(-61, -18);
  context.lineTo(-67, -78);
  context.lineTo(-29, -53);
  context.quadraticCurveTo(0, -65, 29, -53);
  context.lineTo(67, -78);
  context.lineTo(61, -18);
  context.bezierCurveTo(83, 56, -83, 56, -61, -18);
  context.fill();
  context.stroke();
  context.fillStyle = engraved ? "#647d7e" : "#c87551";
  for (const side of [-1, 1]) {
    context.beginPath();
    context.moveTo(side * 57, -60);
    context.lineTo(side * 52, -28);
    context.lineTo(side * 35, -47);
    context.closePath();
    context.fill();
  }
  context.fillStyle = "#233e40";
  for (const side of [-1, 1]) {
    context.beginPath();
    context.ellipse(side * 25, -12, 8, 11, 0, 0, Math.PI * 2);
    context.fill();
    if (!engraved) {
      context.fillStyle = "#ffffff";
      context.beginPath();
      context.arc(side * 25 - 2, -16, 2.5, 0, Math.PI * 2);
      context.fill();
      context.fillStyle = "#233e40";
    }
  }
  context.fillStyle = engraved ? "#516c6e" : "#d27a6c";
  context.beginPath();
  context.moveTo(-8, 6);
  context.lineTo(8, 6);
  context.lineTo(0, 14);
  context.closePath();
  context.fill();
  context.beginPath();
  context.moveTo(0, 14);
  context.quadraticCurveTo(-5, 25, -15, 18);
  context.moveTo(0, 14);
  context.quadraticCurveTo(5, 25, 15, 18);
  for (const side of [-1, 1]) {
    context.moveTo(side * 37, 7);
    context.lineTo(side * 76, 0);
    context.moveTo(side * 38, 18);
    context.lineTo(side * 76, 23);
  }
  context.stroke();
  context.restore();
}

function textureFromCanvas(canvas) {
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 4;
  return texture;
}

function labelTexture(label, color) {
  const canvas = document.createElement("canvas");
  canvas.width = 1536;
  canvas.height = 320;
  const context = canvas.getContext("2d");
  context.fillStyle = color;
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = "#efd69c";
  context.fillRect(0, 5, canvas.width, 7);
  context.fillRect(0, 308, canvas.width, 7);
  // Repeat the cat around the tin so it reads clearly from any approach.
  for (let panel = 0; panel < 3; panel += 1) {
    const x = panel * 512 + 256;
    context.textAlign = "center";
    context.fillStyle = "#fff3d8";
    context.font = "bold 39px sans-serif";
    context.fillText("MEOW", x, 53);
    context.beginPath();
    context.arc(x, 167, 96, 0, Math.PI * 2);
    context.fill();
    catFace(context, x, 183, 1.02);
    context.fillStyle = "#fff3d8";
    context.font = "bold 25px sans-serif";
    context.fillText("CAT FOOD", x, 286);
    context.font = "bold 18px sans-serif";
    context.save();
    context.translate(x + 170, 167);
    context.rotate(Math.PI / 2);
    context.fillText(label, 0, 0, 210);
    context.restore();
  }
  return textureFromCanvas(canvas);
}

function lidTexture() {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 512;
  const context = canvas.getContext("2d");
  context.fillStyle = "#bac9ca";
  context.fillRect(0, 0, 512, 512);
  context.lineWidth = 3;
  for (const radius of [221, 230]) {
    context.strokeStyle = "#8b9f9f";
    context.beginPath();
    context.arc(256, 256, radius, 0, Math.PI * 2);
    context.stroke();
  }
  catFace(context, 256, 337, 1.05, true);
  return textureFromCanvas(canvas);
}

// A self-contained model: the owning level can dispose its geometry/materials.
export function createFoodCan({ label = "SUPPER", boost = false, nutrition = "meal", required = true } = {}) {
  const group = new THREE.Group();
  group.name = "CatFoodCan";
  group.userData.ownsMaterials = true;
  const color = boost ? "#4e783a" : nutrition === "lean" ? "#35788f" : nutrition === "bonus" ? "#795589" : required ? "#247b78" : "#b45736";
  const metal = new THREE.MeshStandardMaterial({ color: 0xbac9ca, roughness: 0.32, metalness: 0.72 });
  const labelMaterial = new THREE.MeshStandardMaterial({ map: labelTexture(label, color), roughness: 0.82, metalness: 0 });
  const lidMaterial = new THREE.MeshStandardMaterial({ map: lidTexture(), roughness: 0.42, metalness: 0.55 });
  const add = (name, geometry, material, y) => {
    const object = new THREE.Mesh(geometry, material);
    object.name = name;
    object.position.y = y;
    object.castShadow = true;
    object.receiveShadow = true;
    group.add(object);
    return object;
  };
  add("CanLabel", new THREE.CylinderGeometry(0.335, 0.335, 0.43, 48, 1, true), labelMaterial, 0.26);
  add("CanBase", new THREE.CylinderGeometry(0.337, 0.337, 0.035, 48), metal, 0.03);
  add("CanLid", new THREE.CylinderGeometry(0.335, 0.335, 0.022, 48), [metal, lidMaterial, metal], 0.487);
  for (const y of [0.038, 0.482]) {
    const rim = add("RolledMetalRim", new THREE.TorusGeometry(0.335, 0.021, 8, 48), metal, y);
    rim.rotation.x = -Math.PI / 2;
  }
  const tab = add("PullTab", new THREE.TorusGeometry(0.064, 0.015, 8, 24), metal, 0.515);
  tab.rotation.x = -Math.PI / 2;
  tab.scale.y = 1.55;
  tab.position.z = -0.105;
  const rivet = add("TabRivet", new THREE.CylinderGeometry(0.025, 0.025, 0.014, 16), metal, 0.509);
  rivet.position.z = -0.012;
  return group;
}
