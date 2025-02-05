
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sarna.middleware import LoggingMiddleware


app = FastAPI()
templates = Jinja2Templates(directory="sarna/templates")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="sarna/static"), name="static")

# Add the logging middleware
app.add_middleware(LoggingMiddleware, rate=1, capacity=5)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    client_host = request.client.host
    return templates.TemplateResponse("index.html", {"request": request, "client_host": client_host})
