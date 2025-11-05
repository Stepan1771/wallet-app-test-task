from tests.mock_operation import MockOperation
from tests.mock_wallet import MockWallet


MOCK_WALLETS_DB = {}
MOCK_OPERATIONS_DB = {}


def reset_mock_db():
    global MOCK_WALLETS_DB, MOCK_OPERATIONS_DB
    MOCK_WALLETS_DB = {}
    MOCK_OPERATIONS_DB = {}


def add_mock_wallet(wallet: MockWallet):
    MOCK_WALLETS_DB[wallet.uuid] = wallet
    return wallet


def add_mock_operation(operation: MockOperation):
    MOCK_OPERATIONS_DB[operation.uuid_wallet] = operation
    return operation


def get_mock_wallet(wallet_uuid: str) -> MockWallet | None:
    return MOCK_WALLETS_DB.get(wallet_uuid)


def get_mock_operation(wallet_uuid: str) -> MockOperation | None:
    return MOCK_OPERATIONS_DB.get(wallet_uuid)


def delete_mock_wallet(wallet_uuid: str) -> bool:
    if wallet_uuid in MOCK_WALLETS_DB:
        del MOCK_WALLETS_DB[wallet_uuid]
        return True
    return False


def get_all_mock_wallets() -> dict[str, MockWallet]:
    return MOCK_WALLETS_DB.copy()







