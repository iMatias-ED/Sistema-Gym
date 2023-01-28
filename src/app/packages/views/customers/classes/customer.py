from typing import Dict, List, Union

from PySide6.QtWidgets import QDateTimeEdit

from ..classes.access_time_by_product import AccessTimeByProduct

class Customer:
    id: int
    ci: int
    ruc: str
    phone: str
    email: str
    genre: int
    full_name: str
    invoice_to: str
    access_time: List[AccessTimeByProduct]

    def __init__(self, customer: Dict[ str, str ]):
        self.ci         = customer["ci"] 
        self.ruc        = customer["ruc"] 
        self.full_name  = customer["full_name"] 
        self.phone      = customer["phone"] 
        self.email      = customer["email"] 
        self.genre      = customer["genre"] 
        self.invoice_to = customer["invoice_to"] 


        if "id" in customer:    self.id = customer["id"]

        self.access_time = []
        if "access_time_from_ui" in customer:
            data: Dict[int, QDateTimeEdit] = customer["access_time_from_ui"]

            for id, date_input in data.items():
                self.add_access_time(AccessTimeByProduct({
                    "id_product": id,
                    "access_until_date": date_input.text
                }))

    def add_access_time(self, access_time: AccessTimeByProduct) -> None:
        self.access_time.append(access_time)

    def access_time_by_product_id(self, product_id: int) -> Union[AccessTimeByProduct, None]:
        try: 
            return [ time for time in self.access_time if time.id_product == product_id ][0]
        except IndexError:
            return None

    def update_access_time_by_product_id(self, product_id: int, new_date: str) -> None:
        time = self.access_time_by_product_id(product_id)
        time.access_until_date = new_date
