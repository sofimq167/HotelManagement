class Cliente:
    def __init__(self, nombre: str, documento: str):
        self.nombre = nombre
        self.documento = documento

    def __str__(self):
        return f"{self.nombre} (ID: {self.documento})"
