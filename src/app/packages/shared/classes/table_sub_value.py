class SubValue:
    column_name_attr: str
    is_column_name_an_attr: bool
    value_attr: str
    
    def __init__(self, column_name: str, value_attr_name: str, is_column_attr: bool = False):
        self.column_name_attr = column_name
        self.value_attr = value_attr_name
        self.is_column_name_an_attr = is_column_attr