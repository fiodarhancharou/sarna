from locust import HttpUser, TaskSet, task, between
import websocket
import json
import threading
import time

class WebSocketTasks(TaskSet):
    @task
    def load_main_page(self):
        self.client.get("/")

    def on_start(self):
        self.ws = websocket.WebSocketApp("ws://localhost:8000/ws",
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.start()
        time.sleep(1)  # Wait for connection to establish

    def on_message(self, ws, message):
        data = json.loads(message)
        if 'progress' in data:
            print(f"Progress: {data['progress']}%")

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket closed")
        self.client.get("/plot_image/10")

    @task
    def send_number(self):
        number = 10  # Example number, you can randomize or parameterize this
        self.ws.send(json.dumps({"number": number}))

    def on_stop(self):
        self.ws.close()
        self.ws_thread.join()

    @task
    def start_process(self):
        self.client.post("/plot", data={"number": 10})


class WebsiteUser(HttpUser):
    tasks = [WebSocketTasks]
    wait_time = between(1, 5)

    def on_start(self):
        self.websocket_tasks = WebSocketTasks(self)
        self.websocket_tasks.on_start()

    def on_stop(self):
        self.websocket_tasks.on_stop()
