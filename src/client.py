import socket
import utils

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

def receive_hand(conn):

    hand_str =  utils.receive_message(conn)

    hand_list = []
    hand_list.append(int(hand_str[5]))
    hand_list.append(int(hand_str[7]))
    hand_list.append(int(hand_str[9]))

    return hand_list

if __name__ == "__main__":
    r = input("Wellcome to PPT2! \nPress <enter> to play or q to quit!").strip().lower()
    if r == 'q':
        print("\nGoodbye!")

    print("\n")

    server_ip = input("\nPor favor, digite o endereço IP do servidor: ")
    ADDR = (server_ip, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Você está conectado! Aguarde o próximo jogador...")

    hand = receive_hand(client)

    for i in range(3):
        print("\n" + "-" * 20 + f" RODADA {i + 1} " + "-" * 20)
        utils.exibir_mao(hand)

        print("\n")
        card = 0
        for i in range(2):
            status = utils.receive_message(client)
            if status == "WAITING OTHER PLAYER'S CARD":
                print("Aguardando o outro jogador...")
            elif status == "SEND CARD":
                card = utils.escolher_carta("Jogador", hand)
                utils.send_message(client, str(card))

        print("\n")
        print(utils.receive_message(client))
        print(f"Você jogou {utils.traduzir(card)}")
        print(utils.receive_message(client))

        input("\nPressione <enter> para continuar.")

    print(utils.receive_message(client))
    print(utils.receive_message(client))
    print(utils.receive_message(client))

