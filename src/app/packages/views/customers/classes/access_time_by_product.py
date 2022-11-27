from datetime import datetime

class AccessTimeByProduct:
    time: str # date in format %d/%m/%Y
    id_product:int
    unix_time:int

    def __init__(self, data: dict):
        self.time = data["time"]
        self.id_product = data["id_product"]
        self.unix_time = data["unix_time"]
