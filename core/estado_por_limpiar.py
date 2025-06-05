"""
Módulo que define los estados concretos de una habitación.
"""

from core.estado_habitacion import EstadoHabitacion

class PorLimpiar(EstadoHabitacion):
    """
    Estado en el que la habitación está esperando limpieza.
    """

    def manejar_estado(self):
        """
        Cambia el estado de la habitación de 'PorLimpiar' a 'Disponible'.
        """
        print(f"Habitación {self.habitacion.numero} ahora está DISPONIBLE.")
        from core.estado_disponible import Disponible
        nuevo_estado = Disponible()
        nuevo_estado.set_habitacion(self.habitacion)
        self.habitacion.cambiar_estado(nuevo_estado)

    def __str__(self):
        """
        Retorna la representación textual del estado.
        """
        return "PorLimpiar"
