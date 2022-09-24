from typing import Dict, List, Tuple

from datetime import datetime

class Customer:
    id: int
    ci: int
    ruc: str
    phone: str
    email: str
    genre: int
    full_name: str
    invoice_to: str
    access_until_date: int

    def __init__(self, customer: Dict[ str, str ]):
        self.ci         = customer["ci"] 
        self.ruc        = customer["ruc"] 
        self.full_name  = customer["full_name"] 
        self.phone      = customer["phone"] 
        self.email      = customer["email"] 
        self.genre      = customer["genre"] 
        self.invoice_to = customer["invoice_to"] 

        if "id" in customer:    self.id = customer["id"]

        self.access_until_date = customer["access_until_date"]

        

