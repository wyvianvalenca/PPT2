import socket
import utils

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)


def escolher_carta(jogador, mao):
    while True:
        try:
            escolha = int(input(f"{jogador}, escolha sua carta: "))
            if escolha in mao:
                mao.remove(escolha)
                return escolha
            else:
                print("Carta inválida! Escolha uma carta da sua mão.")
        except ValueError:
            print("Digite um número válido!")


def receive_hand(conn):
    hand_str = utils.receive_message(conn)

    hand_list = []
    hand_list.append(int(hand_str[5]))
    hand_list.append(int(hand_str[7]))
    hand_list.append(int(hand_str[9]))

    return hand_list


def handle_game():
    hand = receive_hand(client)

    for i in range(3):
        print("\n" + "-" * 20 + f" RODADA {i + 1} " + "-" * 20 + "\n")
        utils.exibir_mao_estilo_rpg(hand)

        print("\n")

        card = 0

        for i in range(2):
            status = utils.receive_message(client)
            if status == "WAITING OTHER PLAYER'S CARD":
                print("Aguardando o outro jogador...")
            elif status == "SEND CARD":
                card = escolher_carta("Jogador", hand)
                utils.send_message(client, str(card))

        print("\n")
        print(utils.receive_message(client))
        print(f"Você jogou {utils.traduzir(card)}")
        print(utils.receive_message(client))

        input("\nPressione <enter> para continuar.")

    print("\n")
    print(utils.receive_message(client))
    print(utils.receive_message(client))
    print(utils.receive_message(client))


def handle_rematch():
    print(utils.receive_message(client))
    response = input("1 - Sim\n2 - Não\n")
    utils.send_message(client, response)
    utils.receive_message(client)

    if response == "REMATCH":
        return True
    else:
        return False


def handle_scoreboard():
    print(utils.receive_message(client))


if __name__ == "__main__":
    r = (
        input("Bem-vindo ao PPT2! \nPressione <enter> para jogar ou q para sair!")
        .strip()
        .lower()
    )
    if r == "q":
        print("\nTchau tchau!")

    print("\n")

    server_ip = input("\nPor favor, digite o endereço IP do servidor: ")
    ADDR = (server_ip, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print("Você está conectado! Aguarde o próximo jogador...")
    playing = True

    while playing:
        handle_game()
        handle_scoreboard()
        playing = handle_rematch()

    print("Fim do jogo")
    print("Tchau tchau!")
