class SummaryContent:
    title: str
    second_title: str
    table_content: list
    table_headers: list[str]
    bottom_label: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)