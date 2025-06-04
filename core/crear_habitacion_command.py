from core import habitacion
from core.comando import Comando

class CrearHabitacionCommand(Comando):
    def __init__(self, tipo, factory, receptor):
        self.tipo = tipo
        self.factory = factory
        self.receptor = receptor

    def ejecutar(self):
        habitacion_creada = self.receptor.crear_habitacion(self.tipo, self.factory)
        return habitacion_creada
