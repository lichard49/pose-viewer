import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let camera;
let scene;
let renderer;
let geometry;

function initViewer() {
  const width = window.innerWidth;
  const height = window.innerHeight;

  // set up camera and scene
  camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 10);
  camera.position.z = 2.5;
  scene = new THREE.Scene();
  scene.add(camera);

  // set up mesh
  geometry = new THREE.BufferGeometry();
  const material = new THREE.MeshNormalMaterial();
  const object = new THREE.Mesh(geometry,  material);
  scene.add(object);

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

initViewer();

function renderPose(faces, vertices) {
  const f = [...faces];
  const v = new THREE.Float32BufferAttribute(vertices, 3);
  geometry.setIndex(f);
  geometry.setAttribute('position',  v);
  geometry.computeVertexNormals();
  geometry.rotateX(Math.PI);

  renderer.render(scene, camera);
}

let pose_faces = null;
let pose_vertices = null;

function setupWebsocket() {
  const origin = window.location.origin;
  const protocol = window.location.protocol;
  const websocketUrl = origin.replace(protocol, 'ws:') + '/ws';

  const websocket = new WebSocket(websocketUrl);
  websocket.binaryType = 'arraybuffer';
  websocket.onmessage = function(event) {
    if (pose_faces === null) {
      pose_faces = new Uint32Array(event.data);
    } else if (pose_vertices === null) {
      pose_vertices = new Float32Array(event.data);
      console.log('render', pose_faces, pose_vertices);
      renderPose(pose_faces, pose_vertices);

      pose_vertices = null;
    }
  };
}

setupWebsocket();
