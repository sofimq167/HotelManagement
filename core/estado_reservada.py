"""
Módulo que define los estados concretos de una habitación.
"""
from core.estado_habitacion import EstadoHabitacion

class Reservada(EstadoHabitacion):
    """
    Estado en el que la habitación ha sido reservada.
    """

    def manejar_estado(self):
        """
        Cambia el estado de la habitación de 'Reservada' a 'Ocupada'.
        """
        print(f"Habitación {self.habitacion.numero} ahora está OCUPADA.")
        from core.estado_ocupada import Ocupada
        nuevo_estado = Ocupada()
        nuevo_estado.set_habitacion(self.habitacion)
        self.habitacion.cambiar_estado(nuevo_estado)

    def __str__(self):
        """
        Retorna la representación textual del estado.
        """
        return "Reservada"
