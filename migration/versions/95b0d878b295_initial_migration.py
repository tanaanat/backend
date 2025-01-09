"""Initial migration

Revision ID: 95b0d878b295
Revises: 
Create Date: 2025-01-09 16:53:19.331395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '95b0d878b295'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 外部キー制約を先に削除
    op.drop_constraint('stats_user_id_fkey', 'stats', type_='foreignkey')
    # stats テーブルを削除
    op.drop_table('stats')
    # users テーブルを削除
    op.drop_table('users')


def downgrade():
    # テーブルの再作成
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=26), primary_key=True),
        sa.Column('username', sa.String(length=255), nullable=False)
    )
    op.create_table(
        'stats',
        sa.Column('id', sa.String(length=26), primary_key=True),
        sa.Column('user_id', sa.String(length=26), sa.ForeignKey('users.id'), nullable=False)
    )
    # ### end Alembic commands ###
