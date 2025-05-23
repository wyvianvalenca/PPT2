import random
from enum import Enum
from collections import Counter
from collections import defaultdict

HEADER = 64
FORMAT = "utf-8"


def send_message(conn, message):
    message = message.encode(FORMAT)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))

    conn.send(send_length)
    conn.send(message)


def receive_message(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)

    if msg_length:
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        return msg

    return None


class Carta(Enum):
    PEDRA = "Pedra"
    PAPEL = "Papel"
    TESOURA = "Tesoura"


def traduzir(carta_numero):
    if 1 <= carta_numero <= 3:
        return Carta.PEDRA
    elif 4 <= carta_numero <= 6:
        return Carta.PAPEL
    elif 7 <= carta_numero <= 9:
        return Carta.TESOURA


def decidir_vencedor(carta1, carta2):
    if carta1 == carta2:
        return 0
    elif (
        (carta1 == Carta.PEDRA and carta2 == Carta.TESOURA)
        or (carta1 == Carta.PAPEL and carta2 == Carta.PEDRA)
        or (carta1 == Carta.TESOURA and carta2 == Carta.PAPEL)
    ):
        return 1
    else:
        return 2


def criar_baralho():
    baralho = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(baralho)
    return baralho


def distribuir_cartas(baralho):
    return baralho[:3], baralho[3:6]


def exibir_mao(mao):
    contagem = Counter([traduzir(c) for c in mao])
    for carta in Carta:
        print(f"{carta.value}: {contagem.get(carta, 0)} carta(s)")
    for carta in sorted(mao):
        print(f" - {carta}: {traduzir(carta)}")


def exibir_mao_estilo_rpg(mao):
    agrupadas = defaultdict(list)
    for carta in mao:
        tipo = traduzir(carta)
        agrupadas[tipo].append(carta)

    print("=" * 22)
    print("      Sua Mão")
    print("=" * 22)
    for tipo in Carta:
        cartas = sorted(agrupadas.get(tipo, []))
        if cartas:
            numeros = ", ".join(str(c) for c in cartas)
        else:
            numeros = "-"
        print(f"{tipo.value:<8}: {numeros}")
    print("=" * 22)


def jogar_rodada(jogador_um, jogador_dois):
    print("Cartas do Jogador 1:")
    exibir_mao(jogador_um)
    escolha_um = escolher_carta("Jogador 1", jogador_um)

    print("\n" + "-" * 30)

    print("Cartas do Jogador 2:")
    exibir_mao(jogador_dois)
    escolha_dois = escolher_carta("Jogador 2", jogador_dois)

    tipo_um = traduzir(escolha_um)
    tipo_dois = traduzir(escolha_dois)

    print(f"\nJogador 1 jogou: {tipo_um.value}")
    print(f"Jogador 2 jogou: {tipo_dois.value}")

    return decidir_vencedor(tipo_um, tipo_dois)


def exibir_resultado_final(placar):
    print("\n==== Resultado Final ====")
    print(f"Jogador 1 venceu {placar['Jogador 1']} rodada(s)")
    print(f"Jogador 2 venceu {placar['Jogador 2']} rodada(s)")

    if placar["Jogador 1"] > placar["Jogador 2"]:
        print("Jogador 1 é o vencedor!")
    elif placar["Jogador 2"] > placar["Jogador 1"]:
        print("Jogador 2 é o vencedor!")
    else:
        print("Empate geral!")


def executar_jogo():
    baralho = criar_baralho()
    jogador_um, jogador_dois = distribuir_cartas(baralho)
    placar = {"Jogador 1": 0, "Jogador 2": 0}

    for rodada in range(3):
        print(f"\n==== Rodada {rodada + 1} ====")
        vencedor = jogar_rodada(jogador_um, jogador_dois)

        if vencedor == 0:
            print("Empate!")
        elif vencedor == 1:
            print("Jogador 1 venceu a rodada!")
            placar["Jogador 1"] += 1
        else:
            print("Jogador 2 venceu a rodada!")
            placar["Jogador 2"] += 1

    exibir_resultado_final(placar)
