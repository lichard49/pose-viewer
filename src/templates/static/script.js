const centerPanel = document.getElementById('center-panel');
const outputCells = centerPanel.getElementsByTagName('output-cell');
const lastOutputCell = outputCells[outputCells.length - 1];

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
  if (event.data instanceof ArrayBuffer) {
    if (poseFaces === null) {
      poseFaces = new Uint32Array(event.data);
    } else if (poseVertices === null) {
      poseVertices = new Float32Array(event.data);

      lastOutputCell.renderPose(poseFaces, poseVertices);

      poseVertices = null;
    }
  }
}

setupWebsocket('pose', poseModeHandler);
