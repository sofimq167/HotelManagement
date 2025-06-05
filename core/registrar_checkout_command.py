"""
Módulo que define el comando para registrar el check-out de una reserva.
"""

from core.comando import Comando

class RegistrarCheckOutCommand(Comando):
    """
    Comando para registrar el check-out de una reserva existente.

    Atributos:
        id_reserva (int): Identificador de la reserva.
        receptor (object): Objeto que contiene la lógica de check-out.
    """

    def __init__(self, id_reserva, receptor):
        """
        Inicializa el comando con el ID de la reserva y el receptor.

        Args:
            id_reserva (int): Identificador de la reserva.
            receptor (object): Objeto que ejecuta el método de check-out.
        """
        super().__init__()
        self.id_reserva = id_reserva
        self.receptor = receptor

    def ejecutar(self):
        """
        Ejecuta el comando para realizar el check-out de la reserva.

        Returns:
            object: Resultado de la operación de check-out.
        """
        return self.receptor.checkout(self.id_reserva)
