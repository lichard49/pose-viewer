from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse


app = FastAPI()

@app.get('/')
async def get():
  return HTMLResponse('hi')
