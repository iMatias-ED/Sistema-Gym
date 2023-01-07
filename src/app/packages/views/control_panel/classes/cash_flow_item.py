
class CashFlowItem:
    user_name: str
    amount: int
    description: str
    date: str

    def __init__(self, data: dict):
        self.user_name = data["user_name"]
        self.amount = data["amount"]
        self.description = data["description"]
        self.date = data["date"]