
class ConfirmationMessage:
    title: str
    message: str
    highlight: str

    def __init__(self, title: str, msg: str, highlight: str):
        self.title = title
        self.message = msg
        self.highlight = highlight