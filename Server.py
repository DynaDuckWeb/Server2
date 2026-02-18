from flask import request
import os
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

clients = {}

@app.route("/")
def home():
    return "🦆 DynaDuck Server Live!"

@socketio.on("connect")
def on_connect():
    print("Duck connected!")

@socketio.on("player_data")
def handle_player_data(data):
    clients[request.sid] = data
    emit("player_update", data, broadcast=True, include_self=False)

@socketio.on("disconnect")
def on_disconnect():
    print("Duck disconnected!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
