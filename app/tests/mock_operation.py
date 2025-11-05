from dataclasses import dataclass
from datetime import datetime


@dataclass
class MockOperation:
    id: int
    uuid_wallet: str
    date_time: datetime
    operation: str
    description: str


    def __init__(
            self,
            id: int = 1,
            uuid_wallet: str = "119D2163-F16A-47AF-9DF7-418D3AF1455A",
            date_time: datetime = datetime.now(),
            operation: str = None,
            description: str = None,
    ):
        self.id = id
        self.uuid_wallet = uuid_wallet
        self.date_time = date_time
        self.operation = operation
        self.description = description