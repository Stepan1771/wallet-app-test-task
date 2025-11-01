from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String, Index

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Operation(IntIdPkMixin, Base):
        __tablename__ = 'operations'

        uuid_wallet: Mapped[str] = mapped_column(
                String(36),
                ForeignKey(
                        'wallets.uuid',
                        ondelete='CASCADE',
                ),
                nullable=False,
                index=True,
        )
        date_time: Mapped[str] = mapped_column(
                DateTime,
                nullable=False,
                index=True,
        )
        operation: Mapped[str] = mapped_column(
                String(20),
                nullable=False,
                index=True,
        )
        description: Mapped[str] = mapped_column(
                String(255),
                nullable=False,
        )

        wallet = relationship(
                "Wallet",
                back_populates="operations"
        )

        __table_args__ = (
                # Для запросов "показать операции кошелька за период"
                Index('idx_operations_wallet_date', 'uuid_wallet', 'date_time'),

                # Для запросов "показать операции определенного типа по дате"
                Index('idx_operations_type_date', 'operation', 'date_time'),

                # Для аналитических запросов по дате
                Index('idx_operations_date', 'date_time'),
        )