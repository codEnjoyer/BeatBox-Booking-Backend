"""slot and person data move to booking

Revision ID: e91f59af6a80
Revises: 8b222c86f64c
Create Date: 2024-05-15 23:06:30.625886

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e91f59af6a80'
down_revision: Union[str, None] = '8b222c86f64c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('bookings_slot_id_fkey', 'bookings', type_='foreignkey')
    op.drop_table('slots')
    op.add_column('bookings', sa.Column('id', sa.UUID(), nullable=False))
    op.add_column('bookings', sa.Column('name', sa.String(), nullable=False))
    op.add_column('bookings', sa.Column('surname', sa.String(), nullable=True))
    op.add_column(
        'bookings',
        sa.Column('starts_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.add_column(
        'bookings',
        sa.Column('ends_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.add_column(
        'bookings', sa.Column('room_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(None, 'bookings', 'rooms', ['room_id'], ['id'])
    op.drop_column('bookings', 'slot_id')
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
    op.drop_column('users', 'surname')
    op.drop_column('users', 'name')
    op.drop_column('users', 'patronymic')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users',
        sa.Column(
            'patronymic', sa.VARCHAR(), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        'users',
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        'users',
        sa.Column('surname', sa.VARCHAR(), autoincrement=False, nullable=False),
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
    op.add_column(
        'bookings',
        sa.Column('slot_id', sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_slot_id_fkey', 'bookings', 'slots', ['slot_id'], ['id']
    )
    op.drop_column('bookings', 'room_id')
    op.drop_column('bookings', 'ends_at')
    op.drop_column('bookings', 'starts_at')
    op.drop_column('bookings', 'surname')
    op.drop_column('bookings', 'name')
    op.drop_column('bookings', 'id')
    op.create_table(
        'slots',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            'start_time',
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            'end_time',
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column('room_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            'is_available',
            sa.BOOLEAN(),
            server_default=sa.text('true'),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['room_id'], ['rooms.id'], name='slots_room_id_fkey'
        ),
        sa.PrimaryKeyConstraint('id', name='slots_pkey'),
    )
    # ### end Alembic commands ###
