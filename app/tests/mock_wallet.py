from dataclasses import dataclass


@dataclass
class MockWallet:
    uuid: str
    balance: float


    def __init__(
            self,
            uuid: str = "119D2163-F16A-47AF-9DF7-418D3AF1455A",
            balance: float = 0,
    ):
        self.uuid = uuid
        self.balance = balance