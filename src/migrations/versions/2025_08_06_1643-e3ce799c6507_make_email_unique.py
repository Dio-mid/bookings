"""make email unique

Revision ID: e3ce799c6507
Revises: 5874c7399d24
Create Date: 2025-08-06 16:43:52.787086

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e3ce799c6507"
down_revision: Union[str, Sequence[str], None] = "5874c7399d24"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])



def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
