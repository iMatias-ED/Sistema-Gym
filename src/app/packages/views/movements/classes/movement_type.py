
class MovementType:
    id: int
    name: str
    description: str
    action: str

    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.action = data["action"]