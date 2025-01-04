from enum import StrEnum

MAX_GUESSES = 6


class GameStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    ABANDONED = "abandoned"
    WON = "won"
    LOST = "lost"


class CompassDirection(StrEnum):
    NORTH = "NORTH"
    NORTH_EAST = "NORTH_EAST"
    EAST = "EAST"
    SOUTH_EAST = "SOUTH_EAST"
    SOUTH = "SOUTH"
    SOUTH_WEST = "SOUTH_WEST"
    WEST = "WEST"
    NORTH_WEST = "NORTH_WEST"
