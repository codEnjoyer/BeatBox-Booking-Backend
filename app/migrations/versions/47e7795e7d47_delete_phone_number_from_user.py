"""delete phone number from user

Revision ID: 47e7795e7d47
Revises: 786c699a13c1
Create Date: 2024-06-14 23:24:58.099532

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '47e7795e7d47'
down_revision: Union[str, None] = '786c699a13c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'studios',
        'latitude',
        existing_type=sa.REAL(),
        type_=sa.Float(precision=8),
        existing_nullable=False,
    )
    op.alter_column(
        'studios',
        'longitude',
        existing_type=sa.REAL(),
        type_=sa.Float(precision=8),
        existing_nullable=False,
    )
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users',
        sa.Column(
            'phone_number',
            sa.VARCHAR(length=20),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.alter_column(
        'studios',
        'longitude',
        existing_type=sa.Float(precision=8),
        type_=sa.REAL(),
        existing_nullable=False,
    )
    op.alter_column(
        'studios',
        'latitude',
        existing_type=sa.Float(precision=8),
        type_=sa.REAL(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
