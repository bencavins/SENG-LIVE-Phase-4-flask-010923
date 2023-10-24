"""add pets

Revision ID: 5696ab55efc8
Revises: 
Create Date: 2023-10-24 10:48:15.762188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5696ab55efc8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pets')
    # ### end Alembic commands ###
