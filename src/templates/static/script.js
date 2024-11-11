import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let camera;
let scene;
let renderer;
let geometry;
let mesh;

function initViewer(g) {
  const width = window.innerWidth;
  const height = window.innerHeight;

  // set up camera and scene
  camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 10);
  camera.position.z = 2.5;
  scene = new THREE.Scene();
  scene.add(camera);

  // set up mesh
  geometry = g;
  const material = new THREE.MeshNormalMaterial();
  mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  // set up renderer
  renderer = new THREE.WebGLRenderer({antialias: true});
  renderer.setSize(width, height);
  renderer.render(scene, camera);
  document.body.appendChild(renderer.domElement);

  // set up controller
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.addEventListener('change', () => {
    renderer.render(scene, camera);
  });
}

function renderPose(faces, vertices) {
  const f = [...faces];
  const v = new THREE.Float32BufferAttribute(vertices, 3);
  geometry.setIndex(f);
  geometry.setAttribute('position',  v);
  geometry.computeVertexNormals();
  geometry.rotateX(Math.PI);

  renderer.render(scene, camera);
}

function renderBox(x, y, z) {
  mesh.rotation.x = y;
  mesh.rotation.y = x;
  mesh.rotation.z = z;

  renderer.render(scene, camera);
}

const modelLoader = document.getElementById('model-loader');

function showModelLoader(show) {
  if (show) {
    modelLoader.style.display = 'block';
  } else {
    modelLoader.style.display = 'none';
  }
}

let pose_faces = null;
let pose_vertices = null;

function setupWebsocket(mode, handler) {
  const origin = window.location.origin;
  const protocol = window.location.protocol;
  const websocketUrl = origin.replace(protocol, 'ws:') + '/ws/output/' + mode;

  const websocket = new WebSocket(websocketUrl);
  websocket.binaryType = 'arraybuffer';
  websocket.onmessage = handler;
}

const modeChooserPanel = document.getElementById('mode-chooser-panel');

function showModeChooserPanel(show) {
  if (show) {
    modeChooserPanel.style.display = 'block';
  } else {
    modeChooserPanel.style.display = 'none';
  }
}

function poseModeHandler(event) {
  if (event.data instanceof ArrayBuffer) {
    if (pose_faces === null) {
      pose_faces = new Uint32Array(event.data);
    } else if (pose_vertices === null) {
      pose_vertices = new Float32Array(event.data);

      showModelLoader(false);
      renderPose(pose_faces, pose_vertices);

      pose_vertices = null;
    }
  }
}

function orientationModeHandler(event) {
  if (event.data instanceof ArrayBuffer) {
    const xyz = new Float32Array(event.data);
    // console.log(xyz);

    showModelLoader(false);
    renderBox(xyz[0], xyz[1], xyz[2]);
  }
}

const poseMode = document.getElementById('pose-mode');
const orientationMode = document.getElementById('orientation-mode');

function handleModeSelection(e) {
  showModeChooserPanel(false);
  showModelLoader(true);

  switch(e.target) {
    case poseMode:
      initViewer(new THREE.BufferGeometry());
      setupWebsocket('pose', poseModeHandler);
      break;
    case orientationMode:
      initViewer(new THREE.BoxGeometry(3, 1, 3));
      setupWebsocket('orientation', orientationModeHandler);
      break;
  }
}

poseMode.addEventListener('click', handleModeSelection);
orientationMode.addEventListener('click', handleModeSelection);
