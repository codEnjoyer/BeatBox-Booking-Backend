"""add domain models

Revision ID: 8b222c86f64c
Revises: 0cd7bed45c0b
Create Date: 2024-05-13 00:03:15.716287

"""

from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8b222c86f64c'
down_revision: Union[str, None] = '0cd7bed45c0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'files',
        sa.Column('name', sa.UUID(), nullable=False),
        sa.Column(
            'extension',
            sa.Enum('JPEG', 'PNG', 'WEBP', name='supportedfileextensions'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('name'),
    )
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('studio_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['studio_id'],
            ['studios.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    op.create_table(
        'additional_services',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'room_images',
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('image_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ['image_id'],
            ['files.name'],
        ),
        sa.ForeignKeyConstraint(
            ['room_id'],
            ['rooms.id'],
        ),
        sa.PrimaryKeyConstraint('room_id', 'image_id'),
    )
    op.create_table(
        'bookings',
        sa.Column(
            'status',
            sa.Enum(
                'WAITING_FOR_PAYMENT',
                'EXPIRED',
                'CANCELED',
                'BOOKED',
                name='bookingstatus',
            ),
            nullable=False,
        ),
        sa.Column('slot_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['slot_id'],
            ['slots.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('slot_id', 'user_id'),
    )
    op.add_column('reviews', sa.Column('room_id', sa.Integer(), nullable=True))
    op.alter_column(
        'reviews',
        'date',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.alter_column(
        'reviews',
        'text',
        existing_type=sa.VARCHAR(length=500),
        type_=sa.Text(),
        nullable=True,
    )
    op.create_foreign_key(None, 'reviews', 'rooms', ['room_id'], ['id'])
    op.add_column('rooms', sa.Column('banner_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'rooms', 'files', ['banner_id'], ['name'])
    op.add_column(
        'slots',
        sa.Column(
            'is_available',
            sa.Boolean(),
            server_default=sa.text('true'),
            nullable=False,
        ),
    )
    op.alter_column(
        'slots',
        'start_time',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        'slots',
        'end_time',
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.drop_constraint('slots_booked_by_id_fkey', 'slots', type_='foreignkey')
    op.drop_column('slots', 'booked_by_id')
    op.add_column(
        'studios', sa.Column('latitude', sa.Float(precision=8), nullable=False)
    )
    op.add_column(
        'studios', sa.Column('longitude', sa.Float(precision=8), nullable=False)
    )
    op.add_column(
        'studios',
        sa.Column('opening_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.add_column(
        'studios',
        sa.Column('closing_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.add_column(
        'studios',
        sa.Column(
            'site_url', sqlalchemy_utils.types.url.URLType(), nullable=True
        ),
    )
    op.add_column(
        'studios',
        sa.Column(
            'contact_phone_number',
            sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20),
            nullable=True,
        ),
    )
    op.add_column(
        'studios', sa.Column('tg', sa.String(length=100), nullable=True)
    )
    op.add_column(
        'studios', sa.Column('vk', sa.String(length=100), nullable=True)
    )
    op.add_column(
        'studios', sa.Column('whats_app', sa.String(length=100), nullable=True)
    )
    op.alter_column(
        'studios',
        'description',
        existing_type=sa.VARCHAR(length=500),
        nullable=True,
    )
    op.create_index(op.f('ix_studios_name'), 'studios', ['name'], unique=False)
    op.add_column('users', sa.Column('name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('surname', sa.String(), nullable=False))
    op.add_column('users', sa.Column('patronymic', sa.String(), nullable=True))
    op.add_column(
        'users',
        sa.Column(
            'phone_number',
            sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20),
            nullable=False,
        ),
    )
    op.alter_column(
        'users',
        'email',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=320),
        existing_nullable=False,
    )
    op.drop_index('ix_users_username', table_name='users')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'users',
        sa.Column(
            'username',
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        'users',
        sa.Column(
            'is_active', sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.alter_column(
        'users',
        'email',
        existing_type=sa.String(length=320),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'patronymic')
    op.drop_column('users', 'surname')
    op.drop_column('users', 'name')
    op.drop_index(op.f('ix_studios_name'), table_name='studios')
    op.alter_column(
        'studios',
        'description',
        existing_type=sa.VARCHAR(length=500),
        nullable=False,
    )
    op.drop_column('studios', 'whats_app')
    op.drop_column('studios', 'vk')
    op.drop_column('studios', 'tg')
    op.drop_column('studios', 'contact_phone_number')
    op.drop_column('studios', 'site_url')
    op.drop_column('studios', 'closing_at')
    op.drop_column('studios', 'opening_at')
    op.drop_column('studios', 'longitude')
    op.drop_column('studios', 'latitude')
    op.add_column(
        'slots',
        sa.Column(
            'booked_by_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        'slots_booked_by_id_fkey', 'slots', 'users', ['booked_by_id'], ['id']
    )
    op.alter_column(
        'slots',
        'end_time',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.alter_column(
        'slots',
        'start_time',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.drop_column('slots', 'is_available')
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.drop_column('rooms', 'banner_id')
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.alter_column(
        'reviews',
        'text',
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=500),
        nullable=False,
    )
    op.alter_column(
        'reviews',
        'date',
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text('now()'),
    )
    op.drop_column('reviews', 'room_id')
    op.drop_table('bookings')
    op.drop_table('room_images')
    op.drop_table('additional_services')
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')
    op.drop_table('files')
    # ### end Alembic commands ###
