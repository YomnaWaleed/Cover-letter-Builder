# ngrok.py
import requests
import time
import threading
from fastapi import FastAPI
import uvicorn
import pyngrok.ngrok as ngrok
import os
from dotenv import load_dotenv

# Load environment variables if you have any
load_dotenv()

# Configuration
FASTAPI_PORT = 8000
NODE_BACKEND_URL = "http://192.168.1.2:3000/update-ngrok-url"  # Replace with actual URL
NGROK_AUTH_TOKEN = os.getenv(
    "NGROK_AUTH_TOKEN", None
)  # Optional if you have ngrok auth token


def start_fastapi():
    """Start the FastAPI server"""
    uvicorn.run("main:app", host="0.0.0.0", port=FASTAPI_PORT, reload=False)


def get_ngrok_url():
    """Get the public ngrok URL"""
    try:
        # You can also use ngrok.get_tunnels() if you prefer
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            if tunnel.proto == "https":
                return tunnel.public_url
    except Exception as e:
        print(f"Error getting ngrok URL: {e}")
    return None


def send_url_to_node(url):
    """Send the ngrok URL to Node.js backend"""
    try:
        payload = {"url": url}
        headers = {"Content-Type": "application/json"}
        res = requests.post(NODE_BACKEND_URL, json=payload, headers=headers)
        print(f"Sent URL to Node.js backend. Status: {res.status_code}")
        return True
    except Exception as e:
        print(f"Failed to send URL to Node.js: {e}")
        return False


def monitor_and_update_url():
    """Monitor ngrok URL and update Node.js backend when it changes"""
    last_url = None
    while True:
        current_url = get_ngrok_url()

        if current_url and current_url != last_url:
            print(f"New ngrok URL detected: {current_url}")
            if send_url_to_node(current_url):
                last_url = current_url
            else:
                print("Retrying in 30 seconds...")
                time.sleep(30)
                continue

        time.sleep(10)  # Check every 10 seconds


if __name__ == "__main__":
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()

    # Set up ngrok if auth token is provided
    if NGROK_AUTH_TOKEN:
        ngrok.set_auth_token(NGROK_AUTH_TOKEN)

    # Start ngrok tunnel
    ngrok_tunnel = ngrok.connect(FASTAPI_PORT, bind_tls=True)
    print(f"Ngrok tunnel created: {ngrok_tunnel.public_url}")

    # Start monitoring the URL
    monitor_and_update_url()
