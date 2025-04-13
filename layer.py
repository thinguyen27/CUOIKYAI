from enum import IntEnum, auto

class Layer(IntEnum):
    GROUND = auto()
    DOCK = auto()
    WALL = auto()
    CRATE = auto()
    CRATE_DOCK = auto()
    PLAYER = auto()
    PLAYER_DOCK = auto()