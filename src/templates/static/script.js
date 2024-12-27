const centerPanel = document.getElementById('center-panel');
const outputCells = centerPanel.getElementsByTagName('output-cell');
let targetOutputCell = outputCells[outputCells.length - 1];

let poseFaces = null;
let poseVertices = null;

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
      // get ready for new pose
      poseFaces = null;

      // add new output cell
      const newOutputCell = document.createElement('output-cell');
      centerPanel.appendChild(newOutputCell);
      targetOutputCell = newOutputCell;
    }
  } else if (event.data instanceof ArrayBuffer) {
    if (poseFaces === null) {
      // first packet contains pose faces
      poseFaces = new Uint32Array(event.data);
    } else if (poseVertices === null) {
      // second and later packets contain pose vertices
      poseVertices = new Float32Array(event.data);
      targetOutputCell.renderPose(poseFaces, poseVertices);

      // get ready for new pose vertices
      poseVertices = null;
    }
  }
}

setupWebsocket('pose', poseModeHandler);
