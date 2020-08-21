from enum import Enum

class Direction(Enum):
    up = 1
    down = 2
    none = 3

def nextFloorTowards(fromFloor, toFloor):
    if (fromFloor < toFloor):
        return fromFloor + 1
    elif (fromFloor > toFloor):
        return fromFloor - 1
    else:
        return fromFloor

def directionTowards(fromFloor, toFloor):
    if (fromFloor < toFloor):
        return Direction.up
    elif (fromFloor > toFloor):
        return Direction.down
    else:
        return Direction.none

def directionToSymbol(direction):
    if (direction == Direction.up):
        return '▲'
    elif (direction == Direction.down):
        return '▼'
    else:
        return '▬'
