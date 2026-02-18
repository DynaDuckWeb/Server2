import os
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}

@app.route("/")
def home():
    return "🦆 DynaDuck Server Live!"

@socketio.on("connect")
def handle_connect():
    print(f"[JOIN] New duck connected: {socketio.server.eio.sid}")
    emit("message", {"msg": "Welcome Duck!"})

@socketio.on("player_data")
def handle_player_data(data):
    sender = socketio.server.eio.sid
    
    # Save latest player state
    clients[sender] = data
    
    # Broadcast to everyone else
    emit("player_update", data, broadcast=True, include_self=False)

@socketio.on("disconnect")
def handle_disconnect():
    sid = socketio.server.eio.sid
    if sid in clients:
        del clients[sid]
    print(f"[LEAVE] Duck disconnected: {sid}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
