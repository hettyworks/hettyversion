"""empty message

Revision ID: 6aa33ef2bf54
Revises: 2651411abfe8
Create Date: 2017-01-17 22:34:12.880285

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.types as ty
from sqlalchemy.dialects.mysql import VARCHAR, TEXT


# revision identifiers, used by Alembic.
revision = '6aa33ef2bf54'
down_revision = '2651411abfe8'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('song','name', type_=VARCHAR(128, charset='utf8'))
    pass


def downgrade():
    op.alter_column('song','name', type_=VARCHAR(128, charset='latin1'))
    pass