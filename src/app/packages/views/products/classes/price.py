from typing import Dict, List, Tuple

class Price:
    id: int
    name: str
    price: int
    valid_for_days: int

    def __init__(self, price: Dict[ str, str ] ):
        self.name = price["name"]
        self.price = price["price"]
        self.valid_for_days = price["valid_for_days"]

        if "id" in price:    self.id = price["id"]

    def __str__(self):
        return f"{self.name}: {self.price}"

