# filepath: /home/fiodar/repositories/sarna/sarna/main.py
import io
import matplotlib.pyplot as plt
from fastapi import FastAPI, Form, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sarna.middleware import LoggingMiddleware
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="sarna/templates")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="sarna/static"), name="static")

# Add the logging middleware
app.add_middleware(LoggingMiddleware, rate=1, capacity=5)

async def sieve_of_eratosthenes(n: int, websocket: WebSocket = None):
    primes = [True] * (n + 1)
    p = 2
    total_steps = n - 1
    current_step = 0
    while p * p <= n:
        if primes[p]:
            for i in range(p * p, n + 1, p):
                primes[i] = False
                current_step += 1
                if websocket:
                    progress = (current_step / total_steps) * 100
                    await websocket.send_json({"progress": progress})
                    #await asyncio.sleep(0.01)  # Simulate computation delay
        p += 1
    if websocket:
        await websocket.send_json({"progress": 100})
    return [p for p in range(2, n + 1) if primes[p]]

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    client_host = request.client.host
    return templates.TemplateResponse("index.html", {"request": request, "client_host": client_host})

@app.post("/plot", response_class=HTMLResponse)
async def plot(request: Request, number: int = Form(...)):
    primes = app.state.primes.get(number)
    if primes is None:
        return HTMLResponse(content="Primes not calculated yet", status_code=404)
    last_10_primes = primes[-10:]
    return templates.TemplateResponse("last_10_primes.html", {"request": request, "last_10_primes": last_10_primes})

@app.get("/plot_image/{number}")
async def plot_image(number: int):
    # Retrieve the primes from the WebSocket calculation
    primes = app.state.primes.get(number)
    if primes is None:
        return HTMLResponse(content="Primes not calculated yet", status_code=404)
    
    fig, ax = plt.subplots()
    ax.scatter(range(len(primes)), primes, c='blue', marker='o', s=1)
    ax.set_title(f"Primes up to {number}")
    ax.set_xlabel("Index")
    ax.set_ylabel("Prime Number")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted")
    try:
        data = await websocket.receive_json()
        print(f"Received data: {data}")
        number = data["number"]
        primes = await sieve_of_eratosthenes(number, websocket)
        app.state.primes[number] = primes
        print(f"Primes calculated and stored for number: {number}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()
        print("WebSocket connection closed")

# Initialize the app state to store primes
app.state.primes = {}
