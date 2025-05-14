import threading
import socket
import sys
import utils
from typing import Tuple, List

## podiam ser flags
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients: List[Tuple[socket.socket, socket._RetAddress]] = []
clients_lock = threading.RLock()

new_client_event = threading.Event()


def game_loop():
    conn1, _ = clients[0]
    score1 = 0
    conn2, _ = clients[1]
    score2 = 0

    print("[GAME] Shuffling and distributing cards...")

    deck = utils.criar_baralho()
    player1_hand, player2_hand = utils.distribuir_cartas(deck)

    # Send cards to players
    utils.send_message(conn1, f"HAND:{','.join(map(str, player1_hand))}")
    utils.send_message(conn2, f"HAND:{','.join(map(str, player2_hand))}")

    for i in range(3):
        print(f"[PLAYER 1 HAND] {player1_hand}")
        print(f"[PLAYER 2 HAND] {player2_hand}")

        print("[WAITING] Waiting for player1`s card...")
        utils.send_message(conn1, "SEND CARD")
        utils.send_message(conn2, "WAITING OTHER PLAYER'S CARD")

        card1 = int(utils.receive_message(conn1))
        player1_hand.remove(card1)

        print("[WAITING] Waiting for player2`s card...")
        utils.send_message(conn1, "WAITING OTHER PLAYER'S CARD")
        utils.send_message(conn2, "SEND CARD")

        card2 = int(utils.receive_message(conn2))
        player2_hand.remove(card2)

        print(f"[GAME] Player1 played {utils.traduzir(card1)}")
        print(f"[GAME] Player2 played {utils.traduzir(card2)}")

        utils.send_message(conn1, f"Seu oponente jogou {utils.traduzir(card2)}")
        utils.send_message(conn2, f"Seu oponente jogou {utils.traduzir(card1)}")

        winner = utils.decidir_vencedor(utils.traduzir(card1), utils.traduzir(card2))
        if winner == 0:
            print("[GAME] Players tied!")
            utils.send_message(conn1, "Empatou!")
            utils.send_message(conn2, "Empatou!")

        print(f"[GAME] Player{winner} won!")
        if winner == 1:
            score1 += 1
            utils.send_message(conn1, "Você GANHOU!")
            utils.send_message(conn2, "Você perdeu...")
        elif winner == 2:
            score2 += 1
            utils.send_message(conn1, "Você perdeu...")
            utils.send_message(conn2, "Você GANHOU!")

    print(f"[PLAYER 1 FINAL SCORE] {score1}")
    print(f"[PLAYER 2 FINAL SCORE] {score2}")

    utils.send_message(conn1, f"Você venceu {score1} partida(s)")
    utils.send_message(conn1, f"Seu oponente venceu {score2} partida(s)")

    utils.send_message(conn2, f"Você venceu {score2} partida(s)")
    utils.send_message(conn2, f"Seu oponente venceu {score1} partida(s)")

    if score1 == score2:
        print("[FINAL RESULT] It's a tie")
        utils.send_message(conn1, "Deu empate geral.")
        utils.send_message(conn2, "Deu empate geral.")
    elif score1 > score2:
        print("[FINAL RESULT] Player1 wins!")
        utils.send_message(conn1, "Você venceu o jogo!")
        utils.send_message(conn2, "Você perdeu o jogo.")
    else:
        print("[FINAL RESULT] Player2 wins!")
        utils.send_message(conn1, "Você perdeu o jogo.")
        utils.send_message(conn2, "Você venceu o jogo!")

    conn1.close()
    clients.pop()
    conn2.close()
    clients.pop()


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

            print("[WAITING] Waiting for other player...")

        elif len(clients) == 2:
            new_client_event.clear()
            print("[GAME] Starting game...")

            """
            for client in clients:
                conn, addr = client
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()

            clients_lock.release()
            break
            """

            game_thread = threading.Thread(target=game_loop)
            game_thread.daemon = True
            game_thread.start()
            break


try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(f"Error creating socket: {e}")

print("[STARTING] Server is starting...")
start()
