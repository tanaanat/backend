"""empty message

Revision ID: beaf7fe6a34d
Revises: 95b0d878b295
Create Date: 2025-01-14 15:35:34.352912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beaf7fe6a34d'
down_revision: Union[str, None] = '95b0d878b295'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.String(length=26), nullable=False),
    sa.Column('game_name', sa.String(length=50), nullable=False),
    sa.Column('tag_line', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matches',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('puuid', sa.String(length=50), nullable=False),
    sa.Column('map_name', sa.String(length=50), nullable=False),
    sa.Column('game_mode', sa.String(length=50), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('kills', sa.Integer(), nullable=False),
    sa.Column('deaths', sa.Integer(), nullable=False),
    sa.Column('assists', sa.Integer(), nullable=False),
    sa.Column('headshot_percentage', sa.Float(), nullable=False),
    sa.Column('user_id', sa.String(length=26), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('match_comments',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('match_id', sa.String(length=50), nullable=True),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('maps')
    op.drop_table('characters')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.VARCHAR(length=26), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='characters_pkey'),
    sa.UniqueConstraint('name', name='characters_name_key')
    )
    op.create_table('maps',
    sa.Column('id', sa.VARCHAR(length=26), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='maps_pkey'),
    sa.UniqueConstraint('name', name='maps_name_key')
    )
    op.drop_table('match_comments')
    op.drop_table('matches')
    op.drop_table('users')
    # ### end Alembic commands ###
