"""
In the previous implementation:
The ATM class exposes all the methods required user interaction.
A modular approach has been taken to define different entities.
Looks SOLID? Not really.

Let’s say a new requirement for the ATM to allow money transfer comes in.
The current design will require modification in the ATM class;
addition or modification of bunch of states and methods handling the
transition b/w them as well as the existing states. This violates the
Open-closed principle

State-related logic is embedded in the ATM class which violates the
Single-responsibility principle.

Since ATM class functions as a finite-state machine, we can incorporate
the State design pattern.
"""
import datetime
from enum import Enum
from typing import Optional


class Card:
    def __init__(self, card_number: int, expiry_date: datetime.date, pin: int):
        self.card_number = card_number
        self.expiry_date = expiry_date
        self.pin = pin

    def authenticate(self, entered_pin):
        return self.pin == entered_pin


class TransactionType(Enum):
    Credit = "Credit"
    Debit = "Debit"


class Transaction:
    def __init__(self, amount: float, transaction_type: TransactionType):
        self.amount = amount
        self.txn_type = transaction_type
        self.dt = datetime.datetime.now()

    def __str__(self) -> str:
        return f"{self.dt} - {self.txn_type} - {self.amount}"


class Account:
    def __init__(self, balance: float):
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.transactions.append(Transaction(amount, TransactionType.Credit))
        self.update_balance(amount)

    def withdraw(self, amount) -> (int, bool):
        if amount <= self.balance:
            self.update_balance(amount)
            self.transactions.append(Transaction(amount, TransactionType.Debit))
            return amount, True
        else:
            print("Insufficient Balance")
            return -1, False

    def update_balance(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance

    def get_transactions(self) -> list:
        return self.transactions


class Cash:
    def __init__(self, amount: float):
        self.amount = amount


class User:
    def __init__(self, card: Card, account: Account, cash: Optional[Cash]):
        self.card = card
        self.account = account
        self.cash = cash

    def insert_card(self):
        return

    @staticmethod
    def enter_pin() -> int:
        return int(input("Enter Pin: "))

    @staticmethod
    def deposit_money():
        cash = Cash(int(input("Insert cash: ")))
        return cash

    @staticmethod
    def withdraw_money():
        return float(input("Enter the amount: "))

    @staticmethod
    def select_operation():
        try:
            value = int(input())
        except:
            raise Exception("Invalid Input")
        return value


class State(Enum):
    Available = "Available"
    Busy = "Busy"


class Operations(Enum):
    Deposit = 1
    Withdraw = 2
    ShowBalance = 3
    ShowTransactions = 4


class ATM:
    def __init__(self, user: User):
        self.user = user
        self.state = State.Available
        self.transaction_type = None
        self.available_cash = 1000

    def _authenticate(self):
        entered_pin = self.user.enter_pin()
        return self.user.card.pin == entered_pin

    def read_card(self):
        self.user.insert_card()
        self.state = State.Busy
        if self._authenticate():
            self.show_menu()
        else:
            return

    def show_menu(self):
        print("Select Operation:")
        print(f"{Operations.Deposit.value}. Deposit")
        print(f"{Operations.Withdraw.value}. Withdraw")
        print(f"{Operations.ShowBalance.value}. Show balance")
        print(f"{Operations.ShowTransactions.value}. Show transactions")
        operation = self.user.select_operation()
        self.perform_action(operation)

    def perform_action(self, op: int):
        if op == 1:
            self.deposit()
        elif op == 2:
            self.withdraw()
        elif op == 3:
            self.show_balance()
        else:
            self.show_transactions()

    def deposit(self):
        cash = self.user.deposit_money()
        self.user.account.update_balance(cash.amount)
        self.update_available_cash(cash.amount)
        self.return_card()

    @staticmethod
    def is_amount_valid(amount: float):
        return bool(amount)

    def withdraw(self):
        amount = self.user.withdraw_money()
        if self.is_amount_valid(amount):
            print("Dispensing cash...")
            cash = Cash(amount)
            self.user.account.update_balance(-amount)
            print("Please collect your cash")
            self.update_available_cash(-amount)
            return cash
        self.return_card()

    def show_balance(self):
        print(self.user.account.get_balance())
        self.return_card()

    def show_transactions(self):
        for transaction in self.user.account.get_transactions():
            print(transaction)
        self.return_card()

    def return_card(self):
        print("Please collect your card")
        self.state = State.Available
        return

    def update_available_cash(self, amount: float):
        self.available_cash += amount
