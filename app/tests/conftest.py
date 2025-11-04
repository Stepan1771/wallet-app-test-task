import asyncio

from datetime import datetime
from typing import AsyncGenerator
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine


from main import main_app
from tests.test_config.test_base import Base
from tests.test_config.test_config import get_db


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Создаёт event loop для всей сессии тестирования.
    Необходимо для корректной работы async фикстур.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """
    Создаёт async engine для тестовой базы данных.
    Scope='session' - создаётся один раз на всю сессию тестов.
    """
    engine = create_async_engine(
        url=str("postgresql+asyncpg://test_user:test_password@localhost:5433/test_wallet"),
        echo=True,  # Установите True для отладки SQL-запросов
        poolclass=NullPool,  # Отключаем пул соединений для тестов
    )

    # Создаём таблицы один раз
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Удаляем таблицы после всех тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Создаёт новую сессию БД для каждого теста с откатом транзакции.
    """

    connection = await test_engine.connect()
    transaction = await connection.begin()

    async_session_maker = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with async_session_maker() as session:
        yield session

        await session.rollback()

    await transaction.rollback()
    await connection.close()



@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Создаёт HTTP клиент для тестирования API.
    Переопределяет зависимость get_db для использования тестовой БД.
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    main_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url="http://test",
    ) as ac:
        yield ac

    main_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_wallet(db_session: AsyncSession):
    """
    Создаёт тестового пользователя в БД.
    Пример - адаптируйте под свою модель User.
    """
    from tests.test_config.test_wallet import Wallet

    wallet = Wallet(
        uuid="test",
        balance=100.0,
    )
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)

    db_session.expunge(wallet)

    return wallet


@pytest_asyncio.fixture
async def test_operation(db_session: AsyncSession, test_wallet):
    """
    Создаёт тестового пользователя в БД.
    Пример - адаптируйте под свою модель User.
    """
    from tests.test_config.test_operation import Operation

    operation = Operation(
        uuid_wallet="test",
        date_time=datetime(2024, 1, 1, 10, 0, 0),
        operation="deposit",
        description="100",
    )
    db_session.add(operation)
    await db_session.commit()
    await db_session.refresh(operation)

    return operation
