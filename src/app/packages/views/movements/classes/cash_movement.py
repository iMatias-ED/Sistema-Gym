class CashMovement:
    id: int
    id_user: int
    id_cash_flow_type: int
    amount: int
    description: str
    date: str

    def __init__(self, data: dict):
        self.id_user = data["id_user"]
        self.id_cash_flow_type = data["id_cash_flow_type"]
        self.amount = data["amount"]
        self.description = data["description"]

        if "id" in data: self.id = data["id"]
        if "date" in data: self.date = data["date"]
