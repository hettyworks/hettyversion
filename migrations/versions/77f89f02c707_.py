"""empty message

Revision ID: 77f89f02c707
Revises: eeb12fbf394a
Create Date: 2017-01-04 20:05:34.973111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77f89f02c707'
down_revision = 'eeb12fbf394a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('band',
    sa.Column('band_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('band_id')
    )
    op.create_table('comment',
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('version_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('version',
    sa.Column('version_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('song_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('version_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('version')
    op.drop_table('comment')
    op.drop_table('band')
    # ### end Alembic commands ###
