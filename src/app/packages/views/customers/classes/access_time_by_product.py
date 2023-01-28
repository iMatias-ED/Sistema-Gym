from datetime import datetime

class AccessTimeByProduct:
    access_until_date: str # date in format %d/%m/%Y
    id_product:int

    def __init__(self, data: dict):
        self.access_until_date = data["access_until_date"]
        self.id_product = data["id_product"]

    def expiration_as_date(self) -> datetime:
        print("aud", self.access_until_date)
        return datetime.strptime(self.access_until_date, "%d/%m/%Y")
