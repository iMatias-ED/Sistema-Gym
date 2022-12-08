from typing import Dict, List, Tuple

class Price:
    id: int
    name: str
    price: int
    valid_for_days: int

    def __init__(self, price: Dict[ str, str ] ):
        self.name = price["name"]
        self.price = price["price"]

        # Only when read from db
        if "id"             in price:    self.id = price["id"]
        if "valid_for_days" in price:    self.valid_for_days = price["valid_for_days"]

    # def __str__(self):
    #     return f"{self.name}: {self.price}"

