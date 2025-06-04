class InvocadorComando:
    def __init__(self, receptor):
        self.comando = None
        self.receptor = receptor

    def establecerComando(self, comando):
        self.comando = comando

    def ejecutarComando(self):
        if self.comando:
            return self.comando.ejecutar()

