# Sarna project
A placeholder for any kind of project to run


Setup project:
```
uv sync --extra dev
```

Run FastAPI server:
```
uv run uvicorn sarna.main:app --reload
```

Expose the app to web:
```
ngrok start sarna
```

Load test with users:
```
uv run locust -f utils/load_test.py
```

Run app in kubernetes
```
kubectl apply -f /home/fiodar/repositories/sarna/deployment.yaml
```
