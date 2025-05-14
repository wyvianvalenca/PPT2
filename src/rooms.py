from enum import Enum
import socket

class RoomStatus(Enum):
    OPEN = 1
    FULL = 2
    CLOSED = 3


class PlayerType(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2
    

class Player:
    def __init__(self, conn:socket.socket, addr: socket._RetAddress, type: PlayerType) -> None:
        self.address: socket._RetAddress = addr
        self.type: PlayerType = type


class GameRoom:
    def __init__(self, id: int, name: str, host, conn) -> None:
        self.id = id
        self.room_name = name
        self.host = Player()
        self.player_2 = 
        self.status: RoomStatus = RoomStatus.OPEN

        pass

