"""
Módulo que define el invocador de comandos.
"""

class InvocadorComando:
    """
    Invocador que ejecuta comandos sobre un receptor.

    Atributos:
        receptor (object): Objeto que ejecuta la lógica de negocio.
        comando (Comando): Comando a ejecutar.
    """

    def __init__(self, receptor):
        """
        Inicializa el invocador con un receptor.

        Args:
            receptor (object): Objeto que recibe las acciones del comando.
        """
        self.comando = None
        self.receptor = receptor

    def establecer_comando(self, comando):
        """
        Establece el comando a ejecutar.

        Args:
            comando (Comando): Instancia del comando a ejecutar.
        """
        self.comando = comando

    def ejecutar_comando(self):
        """
        Ejecuta el comando actual si ha sido establecido.

        Returns:
            object: Resultado de ejecutar el comando, si existe.
        """
        if self.comando:
            return self.comando.ejecutar()
        return None
