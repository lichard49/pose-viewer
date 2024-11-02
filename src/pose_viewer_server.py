from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import time

from pose_utils import loadPoses, FRAME_RATE


app = FastAPI()
app.mount('/static', StaticFiles(directory='./src/templates/static', html=True), name='static')
templates = Jinja2Templates(directory='./src/templates')


@app.get('/')
async def get(request: Request):
  return templates.TemplateResponse(
    name='index.html',
    request=request,
    context={'id': id}
  )


@app.websocket('/ws')
async def websocketEndpoint(websocket: WebSocket):
  await websocket.accept()

  pose_file = './dataset/sit_to_stands-wham_output.pkl'
  pose_faces, pose_vertices = loadPoses(pose_file)

  await websocket.send_bytes(pose_faces.tobytes())
  for vertices in pose_vertices:
    await websocket.send_bytes(vertices.tobytes())
    time.sleep(1./FRAME_RATE)
