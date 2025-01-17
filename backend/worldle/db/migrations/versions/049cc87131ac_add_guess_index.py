"""Add guess index

Revision ID: 049cc87131ac
Revises: 38a1cb5a0df4
Create Date: 2025-01-03 23:22:44.244383

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "049cc87131ac"
down_revision: str | None = "38a1cb5a0df4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("guesses", sa.Column("index", sa.Integer(), nullable=False))
    op.create_unique_constraint("uq_guess_game_index", "guesses", ["game_id", "index"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("uq_guess_game_index", "guesses", type_="unique")
    op.drop_column("guesses", "index")
    # ### end Alembic commands ###
