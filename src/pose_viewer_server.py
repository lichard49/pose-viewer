from fastapi import FastAPI, Request, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import numpy as np


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

  data = np.array([1, 2, 3], dtype=np.uint32)
  await websocket.send_bytes(data.tobytes())
