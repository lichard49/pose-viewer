import * as THREE from 'three';

let camera;
let scene;
let renderer;

function initViewer() {
  const width = window.innerWidth;
  const height = window.innerHeight;

  camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 10);
  scene = new THREE.Scene();
  scene.add(camera);

  renderer = new THREE.WebGLRenderer({antialias: true});
  renderer.setSize(width, height);
  renderer.render(scene, camera);
  document.body.appendChild(renderer.domElement);
}

initViewer();
