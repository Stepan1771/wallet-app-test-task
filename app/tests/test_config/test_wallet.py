from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, Index, String

from tests.test_config.test_base import Base


class Wallet(Base):
        __tablename__ = 'wallets'

        uuid: Mapped[str] = mapped_column(
                String(36),
                primary_key=True,
                unique=True,
                nullable=False,
                index=True,
        )
        balance: Mapped[float] = mapped_column(
                Numeric(scale=2),
                default=0.0,
                nullable=False,
        )

        operations = relationship(
                "Operation",
                back_populates="wallet",
                cascade="all, delete-orphan"
        )

        __table_args__ = (
                Index('idx_wallet_balance', 'balance'),
        )