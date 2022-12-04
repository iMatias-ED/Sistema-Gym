class CashFlowItem:
    id: int
    id_user: int
    id_movement_type: int
    amount: int
    description: str
    date: str

    def __init__(self, data: dict):
        self.id_user = data["id_user"]
        self.id_movement_type = data["id_movement_type"]
        self.amount = data["amount"]
        self.description = data["description"]

        if "id" in data: self.id = data["id"]
        if "date" in data: self.date = data["date"]
