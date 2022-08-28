from typing import Dict, List, Tuple

class Product:
    id: int
    code: str
    name: str
    description: str
    prices: Dict[ str, int ] = {}

    def __init__(self, product: Tuple[ int, str, str, str ]):
        self.id = product[0]
        self.code = product[1]
        self.name = product[2]
        self.description = product[3]

    def save_prices(self, prices: List[Tuple[str, int]]):
        # print('cambiando precios')
        for price in prices:
            #[0] -> Period; [1] -> value
            self.prices[ price[0] ] = price[1]
        # print( f'En el product {self.name}, los precios son: {self.__prices} ' )

    def print_info(self):
        # pass
        print( f'En el product {self.name}, los precios son: {self.prices} ' )