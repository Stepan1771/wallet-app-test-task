from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e032f2b2bb3d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('wallets',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('balance', sa.Numeric(scale=2), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_wallets'))
    )

    op.create_index('idx_wallet_balance', 'wallets', ['balance'], unique=False)
    op.create_index(op.f('ix_wallets_uuid'), 'wallets', ['uuid'], unique=True)

    op.create_table('operations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid_wallet', sa.String(length=36), nullable=False),
    sa.Column('date_time', sa.DateTime(), nullable=False),
    sa.Column('operation', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['uuid_wallet'], ['wallets.uuid'], name=op.f('fk_operations_uuid_wallet_wallets'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_operations'))
    )

    op.create_index('idx_operations_date', 'operations', ['date_time'], unique=False)
    op.create_index('idx_operations_type_date', 'operations', ['operation', 'date_time'], unique=False)
    op.create_index('idx_operations_wallet_date', 'operations', ['uuid_wallet', 'date_time'], unique=False)
    op.create_index(op.f('ix_operations_date_time'), 'operations', ['date_time'], unique=False)
    op.create_index(op.f('ix_operations_id'), 'operations', ['id'], unique=False)
    op.create_index(op.f('ix_operations_operation'), 'operations', ['operation'], unique=False)
    op.create_index(op.f('ix_operations_uuid_wallet'), 'operations', ['uuid_wallet'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_operations_uuid_wallet'), table_name='operations')
    op.drop_index(op.f('ix_operations_operation'), table_name='operations')
    op.drop_index(op.f('ix_operations_id'), table_name='operations')
    op.drop_index(op.f('ix_operations_date_time'), table_name='operations')
    op.drop_index('idx_operations_wallet_date', table_name='operations')
    op.drop_index('idx_operations_type_date', table_name='operations')
    op.drop_index('idx_operations_date', table_name='operations')
    op.drop_table('operations')
    op.drop_index(op.f('ix_wallets_uuid'), table_name='wallets')
    op.drop_index('idx_wallet_balance', table_name='wallets')
    op.drop_table('wallets')
