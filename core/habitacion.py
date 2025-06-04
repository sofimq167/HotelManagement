from core.ihabitacion import IHabitacion

class Habitacion(IHabitacion):
    def __init__(self, numero: int, descripcion: str, precioBase: float):
        self.numero = numero
        self.descripcion = descripcion
        self.precioBase = precioBase
        self.estado = None

    def cambiarEstado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.estado.setHabitacion(self)

    def manejarEstado(self):
        if self.estado:
            self.estado.manejarEstado()

    def getDescripcion(self) -> str:
        return self.descripcion

    def getPrecio(self) -> float:
        return self.precioBase
