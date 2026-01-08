"""fix_tg_id_type

Revision ID: ea67c8f64a0e
Revises: e46a12a71c8a
Create Date: 2026-01-04 21:43:00.277593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ea67c8f64a0e'
down_revision: Union[str, Sequence[str], None] = 'e46a12a71c8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'tg_id',
               existing_type=sa.Integer(),
               type_=sa.BigInteger(),
               existing_nullable=True)

def downgrade() -> None:
    # Возвращаем к Integer (если потребуется откат)
    op.alter_column('users', 'tg_id',
               existing_type=sa.BigInteger(),
               type_=sa.Integer(),
               existing_nullable=True)
