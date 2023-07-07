from enum import IntEnum, Enum

class Side(IntEnum):
    BOTTOM = 0
    LEFT = 1
    TOP = 2
    RIGHT = 3

class AnchorX(IntEnum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2

class AnchorY(IntEnum):
    TOP = 0
    CENTER = 1
    BOTTOM = 2

class Gravity(IntEnum):
    DOWN = 0
    LEFT = 1
    UP = 2
    RIGHT = 3

class Orientation(Enum):
    VERTICAL = 0
    HORIZONTAL = 1

class MemoryPriority(IntEnum):
    ALWAYS_LOAD = 0
    UNLOAD_IF_NEEDED = 1
    ALWAYS_UNLOAD = 2

class BatAction(Enum):
    MOVE = 0
    FLEE = 1