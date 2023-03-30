class Settings:
    def __init__(self, document: dict):
        if document:
            self.doc = document
            for key, value in document.items():
                setattr(self, key, value)

    def __str__(self):
        text = ""
        for key, value in self.doc.items():
            text += f"{str(key)}={str(value)}, "

        return f"Settings({text})"
