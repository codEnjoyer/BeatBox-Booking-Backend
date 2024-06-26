"""rename file columns

Revision ID: a38d4efd6c93
Revises: f5767b10d2ce
Create Date: 2024-06-19 15:20:38.527381

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a38d4efd6c93'
down_revision: Union[str, None] = 'f5767b10d2ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('banner_filename', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('images_filenames', postgresql.ARRAY(sa.String()), server_default='{}', nullable=False))
    op.drop_column('rooms', 'images')
    op.drop_column('rooms', 'banner')
    op.add_column('studios', sa.Column('banner_filename', sa.String(), nullable=True))
    op.alter_column('studios', 'latitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.alter_column('studios', 'longitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.drop_column('studios', 'banner')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('studios', sa.Column('banner', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('studios', 'longitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('studios', 'latitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.drop_column('studios', 'banner_filename')
    op.add_column('rooms', sa.Column('banner', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('rooms', sa.Column('images', postgresql.ARRAY(sa.VARCHAR()), server_default=sa.text("'{}'::character varying[]"), autoincrement=False, nullable=False))
    op.drop_column('rooms', 'images_filenames')
    op.drop_column('rooms', 'banner_filename')
    # ### end Alembic commands ###
