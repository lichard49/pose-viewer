from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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
