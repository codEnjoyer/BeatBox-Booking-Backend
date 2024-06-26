"""delete file

Revision ID: b67f56eae721
Revises: 06b05e039210
Create Date: 2024-06-15 00:39:05.644432

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b67f56eae721'
down_revision: Union[str, None] = '06b05e039210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('room_images')
    op.drop_constraint('rooms_banner_id_fkey', 'rooms', type_='foreignkey')
    op.drop_table('files')
    op.add_column('rooms', sa.Column('banner', sa.String(), nullable=True))
    op.add_column('rooms', sa.Column('images', postgresql.ARRAY(sa.String()), server_default='{}', nullable=False))
    op.drop_column('rooms', 'banner_id')
    op.alter_column('studios', 'latitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.alter_column('studios', 'longitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('studios', 'longitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('studios', 'latitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.add_column('rooms', sa.Column('banner_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_table('files',
    sa.Column('name', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('extension', postgresql.ENUM('JPEG', 'PNG', 'WEBP', name='supportedfileextensions'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('name', name='files_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_foreign_key('rooms_banner_id_fkey', 'rooms', 'files', ['banner_id'], ['name'])
    op.drop_column('rooms', 'images')
    op.drop_column('rooms', 'banner')
    op.create_table('room_images',
    sa.Column('room_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('image_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['files.name'], name='room_images_image_id_fkey'),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], name='room_images_room_id_fkey'),
    sa.PrimaryKeyConstraint('room_id', 'image_id', name='room_images_pkey')
    )
    # ### end Alembic commands ###
