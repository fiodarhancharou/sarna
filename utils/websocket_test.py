# filepath: /home/fiodar/repositories/sarna/test_websocket.py
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        # Send a JSON message to the WebSocket endpoint
        message = {"number": 1000000}
        await websocket.send(json.dumps(message))
        print(f"> Sent: {message}")

        # Receive messages from the WebSocket endpoint
        while True:
            try:
                response = await websocket.recv()
                data = json.loads(response)
                print(f"< Received: {data}")
            except websockets.ConnectionClosed:
                print("WebSocket connection closed")
                break

asyncio.run(test_websocket())
