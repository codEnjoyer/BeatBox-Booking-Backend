"""add max length to strings

Revision ID: b63c8217491c
Revises: f3c425d5ef14
Create Date: 2024-06-25 15:20:52.738024

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b63c8217491c'
down_revision: Union[str, None] = 'f3c425d5ef14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'description',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('rooms', 'equipment',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=512),
               existing_nullable=True)
    op.alter_column('rooms', 'additional_services',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=512),
               existing_nullable=True)
    op.alter_column('studios', 'description',
               existing_type=sa.VARCHAR(length=500),
               type_=sa.String(length=1024),
               existing_nullable=True)
    op.alter_column('studios', 'latitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.alter_column('studios', 'longitude',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=8),
               existing_nullable=False)
    op.alter_column('studios', 'site',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=2083),
               existing_nullable=True)
    op.alter_column('studios', 'contact_phone_number',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=16),
               existing_nullable=True)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.String(length=100),
               type_=sa.VARCHAR(length=200),
               existing_nullable=False)
    op.alter_column('studios', 'contact_phone_number',
               existing_type=sa.String(length=16),
               type_=sa.VARCHAR(length=100),
               existing_nullable=True)
    op.alter_column('studios', 'site',
               existing_type=sa.String(length=2083),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
    op.alter_column('studios', 'longitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('studios', 'latitude',
               existing_type=sa.Float(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('studios', 'description',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
    op.alter_column('rooms', 'additional_services',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
    op.alter_column('rooms', 'equipment',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
    op.alter_column('rooms', 'description',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=500),
               existing_nullable=True)
    # ### end Alembic commands ###
