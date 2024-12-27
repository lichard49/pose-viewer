import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

class OutputCell extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    const root = document.createElement('div');
    root.setAttribute('class', 'output-cell');

    const buttonRow = document.createElement('div');
    const streamButton = document.createElement('button');
    streamButton.setAttribute('class', 'output-cell-button');
    streamButton.textContent = 'stream';
    const uploadButton = document.createElement('button');
    uploadButton.setAttribute('class', 'output-cell-button');
    uploadButton.textContent = 'upload';
    const deleteButton = document.createElement('button');
    deleteButton.setAttribute('class', 'output-cell-button');
    deleteButton.textContent = 'delete';
    deleteButton.addEventListener('click', this.deleteSelf);
    buttonRow.appendChild(streamButton);
    buttonRow.appendChild(uploadButton);
    buttonRow.appendChild(deleteButton);

    root.appendChild(buttonRow);
    this.initViewer()
    this.renderer.domElement.setAttribute('class', 'output-cell-viewer');
    root.appendChild(this.renderer.domElement);
    this.append(root);
  }

  initViewer() {
    const width = 575;
    const height = 575;

    // set up camera and scene
    this.camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 10);
    this.camera.position.z = 2.5;
    this.scene = new THREE.Scene();
    this.scene.add(this.camera);

    // set up mesh
    this.geometry = new THREE.BufferGeometry();
    this.material = new THREE.MeshNormalMaterial();
    this.mesh = new THREE.Mesh(this.geometry, this.material);
    this.scene.add(this.mesh);

    // set up renderer
    this.renderer = new THREE.WebGLRenderer({antialias: true});
    this.renderer.setSize(width, height);
    this.renderer.render(this.scene, this.camera);

    // set up controller
    const controls = new OrbitControls(this.camera, this.renderer.domElement);
    controls.addEventListener('change', () => {
      this.renderer.render(this.scene, this.camera);
    });
  }

  renderPose(faces, vertices) {
    const f = [...faces];
    const v = new THREE.Float32BufferAttribute(vertices, 3);
    this.geometry.setIndex(f);
    this.geometry.setAttribute('position',  v);
    this.geometry.computeVertexNormals();

    this.renderer.render(this.scene, this.camera);
  }

  deleteSelf() {
    const thisOutputCell = this.parentElement.parentElement;
    const outputContainer = this.parentElement.parentElement.parentElement;
    outputContainer.removeChild(thisOutputCell);
  }
}

customElements.define('output-cell', OutputCell);
