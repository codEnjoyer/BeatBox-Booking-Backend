"""studio update

Revision ID: b198f50bc949
Revises: b67f56eae721
Create Date: 2024-06-15 01:02:41.330704

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b198f50bc949'
down_revision: Union[str, None] = 'b67f56eae721'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    op.add_column('studios', sa.Column('banner', sa.String(), nullable=True))
    op.add_column('studios', sa.Column('site', sa.String(length=200), nullable=True))
    op.alter_column('studios', 'latitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.alter_column('studios', 'longitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.drop_column('studios', 'address')
    op.drop_column('studios', 'site_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('studios', sa.Column('site_url', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
    op.add_column('studios', sa.Column('address', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.alter_column('studios', 'longitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('studios', 'latitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.drop_column('studios', 'site')
    op.drop_column('studios', 'banner')
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###
