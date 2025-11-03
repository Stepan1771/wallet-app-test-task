from fastapi import HTTPException


def deposit(
    wallet_balance: float,
    amount: float,
) -> float:
    try:
        new_balance = wallet_balance + amount
        return round(new_balance, 2)

    except Exception as e:
        raise e


def withdraw(
    wallet_balance: float,
    amount: float,
) -> float:
    try:
        if wallet_balance < amount:
            raise HTTPException(status_code=400, detail="Wallet balance must be greater than amount")
        new_balance = wallet_balance - amount
        return round(new_balance, 2)

    except Exception as e:
        raise e
