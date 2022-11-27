from typing import Dict, List, Union

class User:
    id: int
    ci: int
    phone: str
    email: str
    genre: int
    password: str
    full_name: str

    def __init__(self, user: Dict[ str, str ]):
        self.ci         = user["ci"] 
        self.full_name  = user["full_name"] 
        self.phone      = user["phone"] 
        self.email      = user["email"] 
        self.genre      = user["genre"] 
        self.password   = user["password"]

        if "id" in user:    self.id = user["id"]
