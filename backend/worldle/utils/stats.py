from pydantic import BaseModel, Field, computed_field
from sqlalchemy import select
from sqlalchemy.orm import Session

from worldle.db.models import Game, GameStatus
from worldle.utils.game import MAX_GUESSES


class UserStats(BaseModel):
    num_played: int = 0
    num_won: int = 0
    current_streak: int = 0
    max_streak: int = 0
    guess_distribution: dict[int, int] = Field(
        default_factory=lambda: {i + 1: 0 for i in range(MAX_GUESSES)}
    )

    @computed_field
    def win_rate(self) -> float:
        return self.num_won / self.num_played


def get_user_stats(user_client_id: int, session: Session) -> UserStats:
    games = (
        session.execute(
            select(Game)
            .where(Game.user_client_id == user_client_id)
            .where(Game.guesses.any())
        )
        .unique()
        .scalars()
        .all()
    )

    stats = UserStats()
    stats.num_played = len([g for g in games if g.status != GameStatus.IN_PROGRESS])
    stats.num_won = len([g for g in games if g.status == GameStatus.WON])

    # Calculate streaks
    current_streak = 0
    max_streak = 0
    for game in sorted(games, key=lambda g: g.created_at, reverse=True):
        if game.status == GameStatus.WON:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            break

    stats.current_streak = current_streak
    stats.max_streak = max_streak

    # Calculate guess distribution
    for game in games:
        if game.status == GameStatus.WON:
            stats.guess_distribution[len(game.guesses)] += 1

    return stats
