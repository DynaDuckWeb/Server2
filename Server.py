import socket
import threading
from flask import Flask # You might need to pip install flask

# 1. THE WEB PART (For Render to stay awake)
app = Flask(__name__)
@app.route('/')
def home():
    return "DynaDuck Server is Running!"

def run_web():
    # Render provides a 'PORT' environment variable
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 2. THE GAME PART (Your original logic)
UDP_IP = "0.0.0.0"
UDP_PORT = 5005 # Your game port

def run_game():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print("Duck Server Listening...")
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Duck data from {addr}")
        # ... your existing logic to broadcast to other players ...

if __name__ == "__main__":
    # Start the web server in a background thread
    threading.Thread(target=run_web).start()
    # Start the game server
    run_game()
