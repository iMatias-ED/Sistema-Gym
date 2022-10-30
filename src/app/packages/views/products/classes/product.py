from typing import Dict, List

from .price import Price

class Product:
    id: int
    code: str
    name: str
    description: str
    prices: List[Price]

    def __init__(self, product: Dict[ str, str ]):
        self.code = product["code"]
        self.name = product["name"]

        if "description" in product:
            self.description = product["description"]

        if "id" in product:    
            self.id = product["id"]

        self.prices = []

    def get_prices_as_dict():
        pass

    def save_price(self, data: Price):   
        self.prices.append( data )

    def __str__(self):
        str_prices = ""
        for price in self.prices:
            str_prices += f"{price.name}: {price.price}\n"

        return f'''
            code: {self.code}\n
            name: {self.name}\n
            prices: {str_prices}
        '''
