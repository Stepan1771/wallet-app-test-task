from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

import uuid


class UUIDMixin:
    uuid: Mapped[str] = mapped_column(
        String(36),
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
    )