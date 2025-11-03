"""test data

Revision ID: 8747c42bc331
Revises: e032f2b2bb3d
Create Date: 2025-11-01 21:54:55.745666

"""
from typing import Sequence, Union
from datetime import datetime, timedelta
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8747c42bc331'
down_revision: Union[str, Sequence[str], None] = 'e032f2b2bb3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем подключение для выполнения сырых SQL запросов
    conn = op.get_bind()

    # Тестовые кошельки
    wallet_uuids = [
        str(uuid.uuid4()),  # wallet 1
        str(uuid.uuid4()),  # wallet 2
        str(uuid.uuid4()),  # wallet 3
    ]

    # Вставляем тестовые кошельки
    op.bulk_insert(
        sa.table('wallets',
                 sa.column('uuid', sa.String),
                 sa.column('balance', sa.Numeric)
                 ),
        [
            {'uuid': wallet_uuids[0], 'balance': 1500.50},
            {'uuid': wallet_uuids[1], 'balance': 750.25},
            {'uuid': wallet_uuids[2], 'balance': 3000.00},
        ]
    )

    # Генерируем тестовые операции
    operations_data = []
    base_date = datetime(2024, 1, 1, 10, 0, 0)

    # Операции для первого кошелька
    operations_data.extend([
        {
            'uuid_wallet': wallet_uuids[0],
            'date_time': base_date + timedelta(days=i),
            'operation': 'deposit',
            'description': f'amount'
        } for i in range(5)
    ])

    operations_data.extend([
        {
            'uuid_wallet': wallet_uuids[0],
            'date_time': base_date + timedelta(days=10 + i),
            'operation': 'withdraw',
            'description': f'amount'
        } for i in range(3)
    ])

    operations_data.extend([
        {
            'uuid_wallet': wallet_uuids[0],
            'date_time': base_date + timedelta(days=15 + i),
            'operation': 'withdraw',
            'description': f'amount'
        } for i in range(2)
    ])

    # Операции для второго кошелька
    operations_data.extend([
        {
            'uuid_wallet': wallet_uuids[1],
            'date_time': base_date + timedelta(days=2 + i),
            'operation': 'deposit',
            'description': f'amount'
        } for i in range(4)
    ])

    operations_data.extend([
        {
            'uuid_wallet': wallet_uuids[1],
            'date_time': base_date + timedelta(days=12 + i),
            'operation': 'withdraw',
            'description': f'amount'
        } for i in range(3)
    ])

    # Операции для третьего кошелька
    operations_data.extend([
        {
            'uuid_wallet': wallet_uuids[2],
            'date_time': base_date + timedelta(days=5 + i),
            'operation': 'deposit',
            'description': f'amount'
        } for i in range(6)
    ])

    operations_data.extend([
        {
            'uuid_wallet': wallet_uuids[2],
            'date_time': base_date + timedelta(days=20 + i),
            'operation': 'withdraw',
            'description': f'amount'
        } for i in range(2)
    ])

    # Вставляем тестовые операции
    op.bulk_insert(
        sa.table('operations',
                 sa.column('uuid_wallet', sa.String),
                 sa.column('date_time', sa.DateTime),
                 sa.column('operation', sa.String),
                 sa.column('description', sa.String)
                 ),
        operations_data
    )


def downgrade() -> None:
    conn = op.get_bind()

    # Сначала удаляем операции (из-за foreign key constraint)
    conn.execute(sa.text("DELETE FROM operations"))

    # Затем удаляем кошельки
    conn.execute(sa.text("DELETE FROM wallets"))

    print("Тестовые данные успешно удалены")
