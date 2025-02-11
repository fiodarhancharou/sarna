# Sarna project
A placeholder for any kind of project to run


Run FastAPI server:
```
poetry run uvicorn sarna.main:app --reload
```

Expose the app to web:
```
ngrok start sarna
```

Load test with users
```
poetry run locust -f utils/load_test.py
```

Run app in kubernetes
```
kubectl apply -f /home/fiodar/repositories/sarna/deployment.yaml
```
