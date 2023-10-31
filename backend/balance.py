from collections import deque
from datetime import datetime
from icecream import ic

class Participant:
    def __init__(self, name:str, initial_expense:float, concepto:str):
        self.name = name
        self.initial_expense = initial_expense
        self.concepto = concepto
        self.persist_difference = 0
        self.running_difference = 0

class Transaction:
    def __init__(self, from_participant, to_participant, amount):
        self.from_participant = from_participant
        self.to_participant = to_participant
        self.amount = amount

class Barbecue:
    def __init__(self):
        self.bbq_date:str = datetime.strftime(datetime.now(), format="%d-%m-%Y")
        self.participants:dict = {}

    async def add_participant(self, name:str, initial_expense:float, concepto:str=" ") -> None:
        self.participants.update(
            {name: Participant(name, initial_expense, concepto)},
        )

    def delete_participant(self, name:str):
        del self.participants[name]

    @property
    def average_expense(self) -> float:
        try:
            return round(self.total_expense / len(self.participants), 1)
        except ZeroDivisionError:
            return 0
        
    @property
    def num_participants(self) -> int:
        return len(self.participants)

    @property
    def total_expense(self) -> float:
        return round(float(sum(self.participants_initial_expenses.values())), 1)

    @property
    def participants_initial_expenses(self) -> dict:
        partici_init = {}
        for name, obj_participant in self.participants.items():
            partici_init[name] = obj_participant.initial_expense
        return partici_init

    @property
    def participants_initial_expenses_perc(self) -> dict:
        participants_initial_expenses = {}
        for name, obj_participant in self.participants.items():
            try:
                calculo = round(obj_participant.initial_expense / self.total_expense, 2)
            except ZeroDivisionError:
                calculo = 0
            participants_initial_expenses[name] = calculo

        return participants_initial_expenses

    @property
    def get_participants_names(self)-> list[str]:
        return sorted(list(self.participants.keys()))

    def set_participant_differences(self) -> None:
        for name, obj_participant in self.participants.items():
            obj_participant.persist_difference = obj_participant.initial_expense - self.average_expense
            obj_participant.running_difference = obj_participant.initial_expense - self.average_expense

    @property
    def participants_differences(self)-> dict:
        differences = {}
        for name, obj_participant in self.participants.items():
            differences[name] = obj_participant.persist_difference
        return differences

    async def settle_expenses(self)-> list[Transaction]:
        debtors = deque(sorted(
            ((name, participant) for name, participant in self.participants.items() if participant.running_difference < 0),
            key=lambda item: item[1].running_difference
        ))

        #ic(debtors)
        creditors = deque(sorted(
            ((name, participant) for name, participant in self.participants.items() if participant.running_difference > 0),
            key=lambda item: item[1].running_difference, reverse=True
        ))
        #ic(creditors)
        transactions = []

        while debtors and creditors:
            debtor_name, debtor = debtors.popleft()
            creditor_name, creditor = creditors.popleft()

            payment = min(abs(debtor.running_difference), creditor.running_difference)

            transactions.append(Transaction(debtor_name, creditor_name, payment))

            debtor.running_difference += payment
            creditor.running_difference -= payment

            if debtor.running_difference < 0:
                debtors.appendleft((debtor_name, debtor))
            if creditor.running_difference > 0:
                creditors.appendleft((creditor_name, creditor))

        return transactions
    
#! No se usa
def transactions_to_str(transactions:list[Transaction])-> list[str]:
    str_transactions = []
    for transaction in transactions:
        str_transactions.append(f"{transaction.from_participant} debe a {transaction.to_participant} un total de {transaction.amount:.1f} €")

    return str_transactions

if __name__ == '__main__':
    bbq = Barbecue()
    bbq.add_participant('Marion', 71.45, "Comida y aperitivo")
    bbq.add_participant("Leire", 45.2, "postres varios"),
    bbq.add_participant("Sergio", 0)
    transactions_to_str(bbq.settle_expenses())
