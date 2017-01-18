"""empty message

Revision ID: 20788a590941
Revises: 9e35cdfb69b5
Create Date: 2017-01-17 19:28:53.268166

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.types as ty
from sqlalchemy.dialects.mysql import VARCHAR, TEXT


# revision identifiers, used by Alembic.
revision = '20788a590941'
down_revision = '9e35cdfb69b5'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('song','name', type_=VARCHAR(128, charset='utf8'))
    pass


def downgrade():
    op.alter_column('song','name', type_=VARCHAR(128, charset='latin1'))
    pass
