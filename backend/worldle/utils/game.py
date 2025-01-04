from enum import StrEnum

MAX_GUESSES = 6


class GameStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    ABANDONED = "abandoned"
    WON = "won"
    LOST = "lost"
