const centerPanel = document.getElementById('center-panel');
const outputCells = centerPanel.getElementsByTagName('output-cell');
let targetOutputCell = outputCells[outputCells.length - 1];

function setupWebsocket(mode, handler) {
  const origin = window.location.origin;
  const protocol = window.location.protocol;
  const websocketUrl = origin.replace(protocol, 'ws:') + '/ws/output/' + mode;

  const websocket = new WebSocket(websocketUrl);
  websocket.binaryType = 'arraybuffer';
  websocket.onmessage = handler;
}

function poseModeHandler(event) {
  if (typeof event.data === 'string') {
    if (event.data === 'bye') {
      // current target cell is finished being populated...
      // start looping stored animation
      targetOutputCell.startRenderLoop();

      // add new output cell
      const newOutputCell = document.createElement('output-cell');
      centerPanel.appendChild(newOutputCell);
      targetOutputCell = newOutputCell;
    }
  } else if (event.data instanceof ArrayBuffer) {
    if (targetOutputCell.poseFaces === null) {
      // first packet contains pose faces
      targetOutputCell.poseFaces = new Uint32Array(event.data);
    } else {
      // second and later packets contain pose vertices
      const poseVertices = new Float32Array(event.data);
      targetOutputCell.renderPose(targetOutputCell.poseFaces, poseVertices);
      targetOutputCell.poseVertices.push(poseVertices);
    }
  }
}

setupWebsocket('pose', poseModeHandler);
