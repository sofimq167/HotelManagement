from core.notificacion_global import notificador
from core.estado_habitacion import EstadoHabitacion

class Disponible(EstadoHabitacion):
    def manejarEstado(self):
        print(f"Habitación {self.habitacion.numero} ahora está RESERVADA.")
        from core.estados_habitacion import Reservada
        nuevo_estado = Reservada()
        nuevo_estado.setHabitacion(self.habitacion)
        self.habitacion.cambiarEstado(nuevo_estado)
    def __str__(self):
        return "Disponible"

class Reservada(EstadoHabitacion):
    def manejarEstado(self):
        print(f"Habitación {self.habitacion.numero} ahora está OCUPADA.")
        from core.estados_habitacion import Ocupada
        nuevo_estado = Ocupada()
        nuevo_estado.setHabitacion(self.habitacion)
        self.habitacion.cambiarEstado(nuevo_estado)
    def __str__(self):
        return "Reservada"

class Ocupada(EstadoHabitacion):
    def manejarEstado(self):
        print(f"Habitación {self.habitacion.numero} ahora está POR LIMPIAR.")
        from core.estados_habitacion import PorLimpiar
        nuevo_estado = PorLimpiar()
        nuevo_estado.setHabitacion(self.habitacion)
        self.habitacion.cambiarEstado(nuevo_estado)
        notificador.notificar_servicio(self.habitacion, "por_limpiar")
    def __str__(self):
        return "Ocupada"

class PorLimpiar(EstadoHabitacion):
    def manejarEstado(self):
        print(f"Habitación {self.habitacion.numero} ahora está DISPONIBLE.")
        from core.estados_habitacion import Disponible
        nuevo_estado = Disponible()
        nuevo_estado.setHabitacion(self.habitacion)
        self.habitacion.cambiarEstado(nuevo_estado)
    def __str__(self):
        return "PorLimpiar"
