"""created tables event,user,event notification

Revision ID: a2c92cebc84f
Revises: 7a6a59ab341d
Create Date: 2023-10-03 10:16:53.785069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2c92cebc84f'
down_revision = '7a6a59ab341d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('event',
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('organizer_id', sa.Integer(), nullable=False),
    sa.Column('poster', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['organizer_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('event_id')
    )
    op.create_table('event_notification',
    sa.Column('notification_id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
    sa.PrimaryKeyConstraint('notification_id')
    )
    op.create_table('event_user_association',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['event.event_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_user_association')
    op.drop_table('event_notification')
    op.drop_table('event')
    op.drop_table('user')
    # ### end Alembic commands ###
