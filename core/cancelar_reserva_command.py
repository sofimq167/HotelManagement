"""
Módulo que define el comando para cancelar una reserva.
"""
from core.comando import Comando

class CancelarReservaCommand(Comando):
    """
    Comando para cancelar una reserva existente.

    Atributos:
        id_reserva (int): Identificador de la reserva a cancelar.
        receptor (object): Objeto que ejecutará la lógica de cancelación.
    """
    def __init__(self, id_reserva, receptor):
        """
        Inicializa el comando con el ID de la reserva y el receptor.

        Args:
            id_reserva (int): Identificador de la reserva a cancelar.
            receptor (object): Objeto que tiene el método `cancelar_reserva`.
        """
        super().__init__()
        self.id_reserva = id_reserva
        self.receptor = receptor

    def ejecutar(self):
        """
        Ejecuta el comando para cancelar la reserva llamando al receptor.
        """
        return self.receptor.cancelar_reserva(self.id_reserva)