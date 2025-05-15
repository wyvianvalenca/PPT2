# Projeto

## Componentes
- Servidor
    - Endereco
        - Porta
    - Clientes conectados
        - Cliente
    - Sala de jogo
        - Jogo
        - Clientes conectados na sala?

- Cliente
    - Conexao com o servidor
    - sala de jogo conectada
        - host?
        - Jogador
            - Cartas da mao 
            - Carta jogada

- Jogo
    - Deck de cartas
        - Cartas Enviadas para cada jogador
    - Jogadores
        - Jogador 1
        - Jogador 2

    - Partida Atual

    - Rodada Atual
    - Rodadas Totais
- Jogador
    - Cartas da mao
    - Carta escolhida


## Eventos
Servidor:
    - Inicialização do servidor

Cliente:
    - Visualizar salas de jogos
    - Criar Sala de jogo
    - Entrar numa sala de jogo 
    - Fechar Sala de jogo
    - Sair de uma sala de jogo


Jogador
    - Recebe mao de cartas
    - Joga uma carta
    - desiste da partida


Jogo
    - Cria deck da partida
    - distribui cartas para os jogadores
    - recebe cartas jogadas e determina o vencedor
    - 
## Como Funciona a implementação
- Jogos
    - Os jogos serão objetos da class Game, que ira gerenciar o fluxo das partidas
    - Uma partida do jogo seguirá o seguinte fluxo:
        - Fase de compra
            - [Jogo] o jogo irá distribuir para os jogadores as cartas que compoem a sua mao
            - [Jogador] confirma que recebeu as cartas
        - Fase de Batalha
            - [Jogador] escolhera uma carta da mao para devolver para o servidor
            - [Jogo] Valida as cartas devolvidas pelos jogadores e retorna o vencedor da rodada
        - Fase de pontuacao
            - [Jogo] envia de volta as pontuações para os jogadores
            - [Jogo] Pergunta aos jogadores se querem mais uma partida
