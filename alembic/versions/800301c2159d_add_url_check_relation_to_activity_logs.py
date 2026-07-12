"""add url_check relation to activity logs

Revision ID: 800301c2159d
Revises: f8287b390001
Create Date: 2026-07-12 11:51:34.810975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '800301c2159d'
down_revision: Union[str, Sequence[str], None] = 'f8287b390001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'activity_logs',
        sa.Column('url_check_id', sa.Integer(), nullable=True)
    )

    op.create_foreign_key(
        'fk_activity_logs_url_check_id',
        'activity_logs',
        'url_checks',
        ['url_check_id'],
        ['id']
    )


def downgrade() -> None:
    op.drop_constraint(
        'fk_activity_logs_url_check_id',
        'activity_logs',
        type_='foreignkey'
    )

    op.drop_column(
        'activity_logs',
        'url_check_id'
    )