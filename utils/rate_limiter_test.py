import requests
import time

def rate_limiter_test(n_requests: int=10, rate: float=0.1):
    url = "http://127.0.0.1:8000/"
    headers = {"Content-Type": "application/json"}

    # Send multiple requests to test the rate limiter
    for i in range(n_requests):
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            print(f"Request {i + 1}: Rate limit exceeded")
        else:
            print(f"Request {i + 1}: {response.status_code}")
        time.sleep(rate)  # Adjust the sleep time to test different rates

if __name__ == "__main__":
    rate_limiter_test()
