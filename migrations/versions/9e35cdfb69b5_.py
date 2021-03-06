"""empty message

Revision ID: 9e35cdfb69b5
Revises: 1fd8631950ab
Create Date: 2017-01-15 17:43:13.555284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e35cdfb69b5'
down_revision = '1fd8631950ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('version_comment',
    sa.Column('versioncomment_id', sa.Integer(), nullable=False),
    sa.Column('version_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('comment_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['version_id'], ['version.version_id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('versioncomment_id')
    )
    op.create_table('version_comment_vote',
    sa.Column('versioncommentvote_id', sa.Integer(), nullable=False),
    sa.Column('version_id', sa.Integer(), nullable=True),
    sa.Column('voter_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('vote_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['version_id'], ['version.version_id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['voter_id'], ['user.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('versioncommentvote_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('version_comment_vote')
    op.drop_table('version_comment')
    # ### end Alembic commands ###
