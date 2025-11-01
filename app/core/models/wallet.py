from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, Index

from core.models import Base
from core.models.mixins import UUIDMixin


class Wallet(UUIDMixin, Base):
        __tablename__ = 'wallets'

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