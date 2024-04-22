"""Create room model and add foriegn keys

Revision ID: 8ac79b8da155
Revises: eef276f52d7c
Create Date: 2024-04-03 18:33:57.121332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ac79b8da155'
down_revision: Union[str, None] = 'eef276f52d7c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('author_id', sa.Integer(), nullable=False))
    op.add_column('reviews', sa.Column('studio_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'reviews', 'users', ['author_id'], ['id'])
    op.create_foreign_key(None, 'reviews', 'studios', ['studio_id'], ['id'])
    op.create_foreign_key(None, 'rooms', 'studios', ['studio_id'], ['id'])
    op.add_column('slots', sa.Column('room_id', sa.Integer(), nullable=False))
    op.add_column('slots', sa.Column('booked_by_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'slots', 'rooms', ['room_id'], ['id'])
    op.create_foreign_key(None, 'slots', 'users', ['booked_by_id'], ['id'])
    op.drop_column('slots', 'is_free')
    op.add_column('users', sa.Column('email', sa.String(length=100), nullable=False))
    op.drop_index('ix_users_username', table_name='users')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.drop_column('users', 'email')
    op.add_column('slots', sa.Column('is_free', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'slots', type_='foreignkey')
    op.drop_constraint(None, 'slots', type_='foreignkey')
    op.drop_column('slots', 'booked_by_id')
    op.drop_column('slots', 'room_id')
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'studio_id')
    op.drop_column('reviews', 'author_id')
    # ### end Alembic commands ###