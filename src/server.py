import threading
import socket
import sys
from typing import Dict
import utils
from enum import Enum

HEADER_SIZE = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

clients = []
clients_lock = threading.RLock()

new_client_event = threading.Event()


class Results(Enum):
    PLAYER1_WIN = 1
    PLAYER2_WIN = 2
    DRAW = 3


def game(player1: socket.socket, player2: socket.socket) -> Results:
    score1 = 0
    score2 = 0

    print("\n[GAME] Shuffling and distributing cards...")

    deck = utils.criar_baralho()
    player1_hand, player2_hand = utils.distribuir_cartas(deck)

    # Send cards to players
    utils.send_message(player1, f"HAND:{','.join(map(str, player1_hand))}")
    utils.send_message(player2, f"HAND:{','.join(map(str, player2_hand))}")

    for i in range(3):
        print(f"[PLAYER 1 HAND] {player1_hand}")
        print(f"[PLAYER 2 HAND] {player2_hand}")

        print("\n[WAITING] Waiting for player1`s card...")
        utils.send_message(player1, "SEND CARD")
        utils.send_message(player2, "WAITING OTHER PLAYER'S CARD")

        card1 = int(utils.receive_message(player1))
        player1_hand.remove(card1)

        print("\n[WAITING] Waiting for player2`s card...")
        utils.send_message(player1, "WAITING OTHER PLAYER'S CARD")
        utils.send_message(player2, "SEND CARD")

        card2 = int(utils.receive_message(player2))
        player2_hand.remove(card2)

        print(f"\n[GAME] Player1 played {utils.traduzir(card1)}")
        print(f"\n[GAME] Player2 played {utils.traduzir(card2)}")

        utils.send_message(player1, f"Seu oponente jogou {utils.traduzir(card2)}")
        utils.send_message(player2, f"Seu oponente jogou {utils.traduzir(card1)}")

        winner = utils.decidir_vencedor(utils.traduzir(card1), utils.traduzir(card2))
        if winner == 0:
            print("\n[GAME] Players tied!")
            utils.send_message(player1, "Empatou!")
            utils.send_message(player2, "Empatou!")

        print(f"\n[GAME] Player{winner} won!")
        if winner == 1:
            score1 += 1
            utils.send_message(player1, "Você GANHOU!")
            utils.send_message(player2, "Você perdeu...")
        elif winner == 2:
            score2 += 1
            utils.send_message(player1, "Você perdeu...")
            utils.send_message(player2, "Você GANHOU!")

    print(f"\n[PLAYER 1 FINAL SCORE] {score1}")
    print(f"\n[PLAYER 2 FINAL SCORE] {score2}")

    utils.send_message(player1, f"Você venceu {score1} rodada(s)")
    utils.send_message(player1, f"Seu oponente venceu {score2} rodada(s)")

    utils.send_message(player2, f"Você venceu {score2} partida(s)")
    utils.send_message(player2, f"Seu oponente venceu {score1} rodada(s)")

    if score1 == score2:
        print("\n[FINAL RESULT] It's a tie")
        utils.send_message(player1, "Deu empate geral.")
        utils.send_message(player2, "Deu empate geral.")
        return Results.DRAW
    elif score1 > score2:
        print("[FINAL RESULT] Player1 wins!")
        utils.send_message(player1, "Você venceu a partida!")
        utils.send_message(player2, "Você perdeu a partida!")
        return Results.PLAYER1_WIN
    else:
        print("[FINAL RESULT] Player2 wins!")
        utils.send_message(player1, "Você perdeu a partida!")
        utils.send_message(player2, "Você venceu a partida!")
        return Results.PLAYER2_WIN


def rematch(player1: socket.socket, player2: socket.socket):
    utils.send_message(player1, "Voce quer jogar outra partida?")
    utils.send_message(player2, "Voce quer jogar outra partida?")

    utils.receive_message(player1)
    utils.receive_message(player2)

    return True


def scoreboard(player1: socket.socket, player2: socket.socket, scores: Dict):
    partidas = 0
    for _, v in scores.items():
        partidas += v

    score_str = f"[PLACAR]\nJogador 1: {scores['player 1']}\nJogador 2: {scores['player 2']}\nEmpates: {scores['draws']}\n Partidas jogadas: {partidas}"
    print(score_str)
    utils.send_message(player1, score_str)
    utils.send_message(player2, score_str)


def game_loop():
    conn1, _ = clients[0]
    scores = {"player 1": 0, "player 2": 0, "draws": 0}
    conn2, _ = clients[1]

    playing = True
    while playing:
        result = game(player1=conn1, player2=conn2)

        match result:
            case Results.PLAYER1_WIN:
                scores["player 1"] += 1
            case Results.PLAYER2_WIN:
                scores["player 2"] += 1
            case Results.DRAW:
                scores["draws"] += 1

        scoreboard(conn1, conn2, scores)

        playing = rematch(player1=conn1, player2=conn2)

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

    if server is None:
        print("Could not open socket")
        sys.exit(1)

    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"\n[NEW CONNECTION] {addr} connected.")

        with clients_lock:
            if len(clients) < 2:
                clients.append((conn, addr))
                new_client_event.set()

            if len(clients) == 1:
                thread = threading.Thread(target=start_game_when_two_clients)
                thread.daemon = True
                thread.start()

            print(f"\n[ACTIVE CONNECTIONS] {len(clients)}")


def start_game_when_two_clients():
    print("\n[WAITING] Waiting for other player...")

    while True:
        clients_lock.acquire()
        if len(clients) == 1:
            clients_lock.release()
            new_client_event.clear()
            conn, addr = clients[0]

        elif len(clients) == 2:
            new_client_event.clear()
            print("\n[GAME] Starting game...")

            game_thread = threading.Thread(target=game_loop)
            game_thread.daemon = True
            game_thread.start()
            break


try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print(f"Error creating socket: {e}")
    sys.exit(1)

print("[STARTING] Server is starting...")
start()
