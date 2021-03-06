"""empty message

Revision ID: 09184d6a0857
Revises: f352355bb8b1
Create Date: 2018-05-24 04:34:04.029966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09184d6a0857'
down_revision = 'f352355bb8b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('time_report')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('time_report',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created', sa.DATETIME(), nullable=False),
    sa.Column('modified', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
