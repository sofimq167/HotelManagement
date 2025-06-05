"""
Módulo que define el comando para crear una reserva.
"""

from core.comando import Comando

class CrearReservaCommand(Comando):
    """
    Comando para crear una reserva de habitación para un cliente.
    """
    def __init__(self, cliente, habitacion, fecha_inicio, fecha_fin, receptor):
        """
        Inicializa el comando con los datos necesarios para crear una reserva.

        Args:
            cliente (object): Cliente que realiza la reserva.
            habitacion (object): Habitación que se desea reservar.
            fecha_inicio (date): Fecha de inicio.
            fecha_fin (date): Fecha de finalización.
            receptor (object): Objeto que ejecuta la creación de la reserva.
        """
        super().__init__()
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.receptor = receptor

    def ejecutar(self):
        """
        Ejecuta el comando para crear una reserva.

        Returns:
            object: La reserva creada.
        """
        return self.receptor.crear_reserva(
            self.cliente,
            self.habitacion,
            self.fecha_inicio,
            self.fecha_fin
        )
