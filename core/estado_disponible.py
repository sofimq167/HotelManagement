"""
Módulo que define los estados concretos de una habitación.
"""

from core.estado_habitacion import EstadoHabitacion

class Disponible(EstadoHabitacion):
    """
    Estado en el que la habitación está disponible para reserva.
    """

    def manejar_estado(self):
        """
        Cambia el estado de la habitación de 'Disponible' a 'Reservada'.
        """
        from core.estado_reservada import Reservada
        print(f"Habitación {self.habitacion.numero} ahora está RESERVADA.")
        nuevo_estado = Reservada()
        nuevo_estado.set_habitacion(self.habitacion)
        self.habitacion.cambiar_estado(nuevo_estado)

    def __str__(self):
        """
        Retorna la representación textual del estado.
        """
        return "Disponible"
