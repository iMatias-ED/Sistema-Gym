from typing import Dict, List, Tuple

class Period:
    id: int
    name: str
    valid_for_days: str

    def __init__(self, period: Dict[ str, str ] ):
        self.name = period["name"]
        self.description = period["valid_for_days"]

        if "id" in period:    self.id = period["id"]

