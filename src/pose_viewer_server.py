from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount('/static', StaticFiles(directory='./src/templates/static', html=True), name='static')
templates = Jinja2Templates(directory='./src/templates')
output_websocket = None


@app.get('/')
async def get(request: Request):
  return templates.TemplateResponse(
    name='index.html',
    request=request,
    context={'id': id}
  )


@app.websocket('/ws/input/{mode}')
async def inputWebsocketEndpoint(websocket: WebSocket, mode: str):
  await websocket.accept()

  try:
    while websocket:
      # receive data from input websocket
      data = await websocket.receive_bytes()

      if output_websocket is not None:
        # pass it on to output websocket if possible
        await output_websocket.send_bytes(data)
      else:
        print('no output client to send data to')

  except (WebSocketDisconnect, ConnectionClosed):
    print('input client disconnected')
    if output_websocket is not None:
      await output_websocket.send_text('bye')


@app.websocket('/ws/output/{mode}')
async def outputWebsocketEndpoint(websocket: WebSocket, mode: str):
  global output_websocket

  await websocket.accept()
  output_websocket = websocket

  try:
    # keep socket alive
    while websocket:
      await websocket.receive_bytes()

  except (WebSocketDisconnect, ConnectionClosed):
    print('output client disconnected')
