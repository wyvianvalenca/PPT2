import threading
import socket
import sys

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

clients = []
clients_lock = threading.RLock()

new_client_event = threading.Event()

played_cards_p1 = [0, 0, 0]
played_cards_index_p1 = -1
played_cards_p2 = [0, 0, 0]
played_cards_index_p2 = -1

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(f"Error creating socket: {e}")


def handle_client(conn, addr):
    print(f"\n[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")

    conn.close()


def start():
    try:
        server.bind(ADDR)
        server.listen()
    except socket.error as e:
        server.close()
        print(e)
        sys.exit(1)
    else:
        if server is None:
            print("Could not open socket")
            sys.exit(1)

        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()

            with clients_lock:
                if len(clients) < 2:
                    clients.append((conn, addr))
                    new_client_event.set()

                if len(clients) == 1:
                    thread = threading.Thread(target=start_game_when_two_clients)
                    thread.daemon = True
                    thread.start()

                print(f"[ACTIVE CONNECTIONS] {len(clients)}")

def start_game_when_two_clients():
    while True:
        clients_lock.acquire()
        if len(clients) == 1:
            clients_lock.release()
            new_client_event.clear()
            conn, addr = clients[0]

            print ("[WAITING] Waiting for other player...")

        elif len(clients) == 2:
            new_client_event.clear()
            print("[GAME] Starting game...")

            for client in clients:
                conn, addr = client
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()

            clients_lock.release()
            break

print("[STARTING] Server is starting...")
start()
