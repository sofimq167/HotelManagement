"""
Módulo que define los estados concretos de una habitación.
"""
from core.notificacion_global import notificador
from core.estado_habitacion import EstadoHabitacion

class Ocupada(EstadoHabitacion):
    """
    Estado en el que la habitación está ocupada por un huésped.
    """

    def manejar_estado(self):
        """
        Cambia el estado de la habitación de 'Ocupada' a 'PorLimpiar'
        y notifica al servicio de limpieza.
        """
        print(f"Habitación {self.habitacion.numero} ahora está POR LIMPIAR.")
        from core.estado_por_limpiar import PorLimpiar
        nuevo_estado = PorLimpiar()
        nuevo_estado.set_habitacion(self.habitacion)
        self.habitacion.cambiar_estado(nuevo_estado)
        notificador.notificar_servicio(self.habitacion, "por_limpiar")

    def __str__(self):
        """
        Retorna la representación textual del estado.
        """
        return "Ocupada"
