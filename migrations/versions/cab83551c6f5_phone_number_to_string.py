"""Phone number to string

Revision ID: cab83551c6f5
Revises: 72dd7cfbd5fe
Create Date: 2024-06-11 15:26:55.061488

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'cab83551c6f5'
down_revision: Union[str, None] = '72dd7cfbd5fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('studios', 'latitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.alter_column('studios', 'longitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.alter_column('studios', 'contact_phone_number',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('studios', 'contact_phone_number',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
    op.alter_column('studios', 'longitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('studios', 'latitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
