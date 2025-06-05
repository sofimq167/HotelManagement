"""
Módulo que define el comando para registrar el check-in de una reserva.
"""

from core.comando import Comando

class RegistrarCheckInCommand(Comando):
    """
    Comando para registrar el check-in de una reserva existente.

    Atributos:
        id_reserva (int): Identificador de la reserva.
        receptor (object): Objeto que contiene la lógica de check-in.
    """

    def __init__(self, id_reserva, receptor):
        """
        Inicializa el comando con el ID de la reserva y el receptor.

        Args:
            id_reserva (int): Identificador de la reserva.
            receptor (object): Objeto que ejecuta el método de check-in.
        """
        super().__init__()
        self.id_reserva = id_reserva
        self.receptor = receptor

    def ejecutar(self):
        """
        Ejecuta el comando para realizar el check-in de la reserva.

        Returns:
            object: Resultado de la operación de check-in.
        """
        return self.receptor.checkin(self.id_reserva)
