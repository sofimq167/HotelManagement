"""Módulo que define el comando para crear una habitación."""

from core.comando import Comando

class CrearHabitacionCommand(Comando):
    """
    Comando para crear una nueva habitación.

    Atributos:
        tipo (str): Tipo de habitación a crear.
        factory (object): Fábrica para instanciar la habitación.
        receptor (object): Objeto que ejecuta la lógica de creación.
    """

    def __init__(self, tipo, factory, receptor):
        """
        Inicializa el comando para crear una habitación.

        Args:
            tipo (str): Tipo de habitación.
            factory (object): Fábrica que genera la instancia de la habitación.
            receptor (object): Objeto que contiene la lógica de creación.
        """
        super().__init__()
        self.tipo = tipo
        self.factory = factory
        self.receptor = receptor

    def ejecutar(self):
        """
        Ejecuta el comando para crear una habitación.

        Returns:
            object: La habitación creada.
        """
        habitacion_creada = self.receptor.crear_habitacion(self.tipo, self.factory)
        return habitacion_creada
