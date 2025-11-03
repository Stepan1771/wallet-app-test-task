from fastapi import HTTPException


class OperationUtils:
    def __init__(
            self,
            operation_type: str,
            wallet_balance: float,
            amount: float,
    ):
        self.operation_type = operation_type
        self.wallet_balance = wallet_balance
        self.amount = amount


    def execute_operation(self) -> float:
        new_balance = None
        if self.operation_type == "deposit":
            new_balance = self.deposit()
        elif self.operation_type == "withdraw":
            new_balance = self.withdraw()

        return new_balance


    def deposit(self) -> float:
        try:
            new_balance = self.wallet_balance + self.amount
            return round(new_balance, 2)

        except Exception as e:
            raise e


    def withdraw(self) -> float:
        try:
            if self.wallet_balance < self.amount:
                raise HTTPException(status_code=400, detail="Wallet balance must be greater than amount")
            new_balance = self.wallet_balance - self.amount
            return round(new_balance, 2)

        except Exception as e:
            raise e
