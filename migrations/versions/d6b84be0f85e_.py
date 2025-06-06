"""empty message

Revision ID: d6b84be0f85e
Revises: c139bc105dbb
Create Date: 2024-10-21 18:16:17.177035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6b84be0f85e'
down_revision = 'c139bc105dbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('challenges', sa.Column('deploy_status', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('challenges', 'deploy_status')
    # ### end Alembic commands ###
