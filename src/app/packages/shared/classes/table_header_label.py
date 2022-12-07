
class TableHeaderLabel:
    column_name: str
    label: str

    def __init__(self, name:str, label:str):
        self.column_name = name
        self.label = label