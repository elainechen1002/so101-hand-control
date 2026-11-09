import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import URDFLoader from 'urdf-loader';

const status = document.querySelector('#status');
const controlsPanel = document.querySelector('#joint-controls');
const viewReset = document.querySelector('#view-reset');
const host = document.querySelector('#scene');
let failed = false;
function fail(message) {
  failed = true;
  status.textContent = message;
  status.classList.add('error');
  controlsPanel.disabled = true;
  viewReset.disabled = true;
}

try {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#edf0eb');
  const camera = new THREE.PerspectiveCamera(38, 1, 0.005, 20);
  camera.up.set(0, 0, 1); // URDF uses Z up.
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  host.appendChild(renderer.domElement);
  renderer.domElement.setAttribute('aria-label', 'SO-101 model. Use joint sliders to change its pose.');
  renderer.domElement.addEventListener('webglcontextlost', event => {
    event.preventDefault();
    fail('Graphics context lost. Reload this page to restore the viewer.');
  });
  const orbit = new OrbitControls(camera, renderer.domElement);
  orbit.minDistance = 0.15;
  orbit.maxDistance = 3;
  // No automatic rotation or easing: render only when something changes.
  function render() { renderer.render(scene, camera); }
  orbit.addEventListener('change', render);
  function resetView() {
    camera.position.set(0.65, -0.8, 0.55);
    orbit.target.set(0, 0, 0.18);
    orbit.update();
    render();
  }
  viewReset.addEventListener('click', resetView);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x68796d, 2.6));
  const light = new THREE.DirectionalLight(0xffffff, 3);
  light.position.set(1, -2, 3);
  scene.add(light);
  const grid = new THREE.GridHelper(1.2, 24, 0xb0bbb0, 0xd4dbd2);
  grid.rotation.x = Math.PI / 2;
  grid.position.z = -0.005;
  scene.add(grid);
  const resize = new ResizeObserver(() => {
    const { width, height } = host.getBoundingClientRect();
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
    render();
  });
  resize.observe(host);
  resetView();

  let robot;
  const manager = new THREE.LoadingManager();
  manager.onError = url => fail(`Could not load model asset: ${url}. Check the files and reload.`);
  manager.onLoad = () => {
    if (failed || !robot) return;
    controlsPanel.disabled = false;
    viewReset.disabled = false;
    status.textContent = 'Official SO-101 follower · 6 movable joints';
    render();
  };
  const loader = new URDFLoader(manager);
  loader.parseCollision = false;
  loader.load('./models/SO101/so101_new_calib.urdf', loaded => {
    robot = loaded;
    scene.add(robot);
    const order = ['shoulder_pan', 'shoulder_lift', 'elbow_flex', 'wrist_flex', 'wrist_roll', 'gripper'];
    const sliders = [];
    for (const name of order) {
      const joint = robot.joints[name];
      if (!joint || joint.jointType !== 'revolute') throw new Error(`Missing revolute joint: ${name}`);
      const row = document.createElement('div');
      row.className = 'joint';
      const low = THREE.MathUtils.radToDeg(joint.limit.lower);
      const high = THREE.MathUtils.radToDeg(joint.limit.upper);
      const label = name.replaceAll('_', ' ').replace(/^./, c => c.toUpperCase());
      row.innerHTML = `<div class="joint-head"><label for="${name}">${label}</label><output for="${name}">0.0°</output></div>
        <input id="${name}" type="range" min="${low}" max="${high}" step="any" value="0">
        <div class="range"><span>${low.toFixed(1)}°</span><span>${high.toFixed(1)}°</span></div>`;
      const input = row.querySelector('input');
      const output = row.querySelector('output');
      function update() {
        robot.setJointValue(name, THREE.MathUtils.degToRad(Number(input.value)));
        const actual = THREE.MathUtils.radToDeg(joint.angle);
        output.value = `${actual.toFixed(1)}°`;
        input.setAttribute('aria-valuetext', `${actual.toFixed(1)} degrees`);
        render();
      }
      input.addEventListener('input', update);
      // Explicit keyboard increments retain exact URDF endpoints with step="any".
      input.addEventListener('keydown', event => {
        const deltas = { ArrowRight: 1, ArrowUp: 1, ArrowLeft: -1, ArrowDown: -1, PageUp: 10, PageDown: -10 };
        if (!(event.key in deltas) && event.key !== 'Home' && event.key !== 'End') return;
        event.preventDefault();
        const value = event.key === 'Home' ? low : event.key === 'End' ? high : Number(input.value) + deltas[event.key];
        input.value = String(Math.max(low, Math.min(high, value)));
        update();
      });
      document.querySelector('#sliders').appendChild(row);
      sliders.push({ input, update });
      update();
    }
    document.querySelector('#pose-reset').addEventListener('click', () => {
      for (const { input, update } of sliders) { input.value = '0'; update(); }
    });
  }, undefined, error => fail(`Could not load the SO-101 model: ${error.message || error}`));
} catch (error) {
  fail(`Viewer could not start: ${error.message}. Use a browser with WebGL enabled.`);
}
