from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models.user_role import UserRole

revision = 'f1ef34d5f7e6'
down_revision = None


def upgrade() -> None:
    # 1. create enum type
    user_role_enum = sa.Enum(UserRole, name="userrole")
    user_role_enum.create(op.get_bind())

    # 2. convert column from string → enum
    op.alter_column(
        "users",
        "role",
        type_=user_role_enum,
        postgresql_using="role::text::userrole"
    )


def downgrade() -> None:
    # back to string
    op.alter_column(
        "users",
        "role",
        type_=sa.String()
    )

    # drop enum type
    sa.Enum(name="userrole").drop(op.get_bind())