import socket
import threading
import os

# Render needs a web port to stay 'Live'
WEB_PORT = int(os.environ.get("PORT", 8080))
GAME_PORT = 5005 

def handle_client(conn, addr):
    print(f"[NEW DUCK] {addr} connected.")
    while True:
        try:
            data = conn.recv(1024)
            if not data: break
            # Logic to broadcast data to other players goes here
        except:
            break
    conn.close()

def run_game_server():
    # TCP Socket for Render compatibility
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", GAME_PORT))
    server.listen()
    print(f"Game Server listening on port {GAME_PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    # Start the game server in a thread
    threading.Thread(target=run_game_server, daemon=True).start()
    
    # Keep the main thread alive for Render's web check
    # This tricks Render into thinking it's a website so it stays online
    web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_sock.bind(("0.0.0.0", WEB_PORT))
    web_sock.listen()
    while True:
        conn, addr = web_sock.accept()
        conn.send(b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nDuck is Live")
        conn.close()
