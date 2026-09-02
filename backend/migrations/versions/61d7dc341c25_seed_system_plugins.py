"""seed system plugins

Revision ID: 61d7dc341c25
Revises: fbef89a1c714
Create Date: 2026-09-01 23:33:17.562915

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '61d7dc341c25'
down_revision: Union[str, Sequence[str], None] = 'fbef89a1c714'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        INSERT INTO plugins (
            key,
            name,
            icon,
            description,
            color_theme
        )
        VALUES
            (
                'expense',
                'Expense',
                'wallet',
                'Track your expenses',
                'green'
            ),
            (
                'saving',
                'Saving',
                'piggy-bank',
                'Track your savings',
                'blue'
            ),
            (
                'investment',
                'Investment',
                'chart',
                'Track your investments',
                'purple'
            );
    """)


def downgrade() -> None:
    op.execute("""
        DELETE FROM plugins
        WHERE key IN (
            'expense',
            'saving',
            'investment'
        );
    """)