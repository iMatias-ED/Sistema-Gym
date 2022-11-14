from .product_selection import ProductSelection

class SelectedProductInfo:
    row: int
    data: ProductSelection

    def __init__(self, data: ProductSelection, row:int):
        self.row = row
        self.data = data

    def __str__(self):
        return f"{self.row}:{self.data}"