"""empty message

Revision ID: bf8cfb6e1a4b
Revises: 6aa33ef2bf54
Create Date: 2017-01-17 22:35:44.760223

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.types as ty
from sqlalchemy.dialects.mysql import VARCHAR, TEXT


# revision identifiers, used by Alembic.
revision = 'bf8cfb6e1a4b'
down_revision = '6aa33ef2bf54'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('venue','name', type_=VARCHAR(128, charset='utf8'))
    pass


def downgrade():
    op.alter_column('venue','name', type_=VARCHAR(128, charset='latin1'))
    pass