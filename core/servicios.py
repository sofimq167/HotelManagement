from core.ihabitacion import IHabitacion
from abc import ABC

class ServicioAdicional(IHabitacion, ABC):
    def __init__(self, habitacion: IHabitacion):
        self.habitacion = habitacion

    def getDescripcion(self) -> str:
        return self.habitacion.getDescripcion()

    def getPrecio(self) -> float:
        return self.habitacion.getPrecio()

    @property
    def numero(self):
        return self.habitacion.numero

    @property
    def descripcion(self):
        return self.habitacion.descripcion

    @property
    def precioBase(self):
        return self.habitacion.precioBase

class ServicioRestaurante(ServicioAdicional):
    def getDescripcion(self) -> str:
        return self.habitacion.getDescripcion() + " + Servicio Restaurante"

    def getPrecio(self) -> float:
        return self.habitacion.getPrecio() + 30

class ServicioAsistencia(ServicioAdicional):
    def getDescripcion(self) -> str:
        return self.habitacion.getDescripcion() + " + Servicio Asistencia"

    def getPrecio(self) -> float:
        return self.habitacion.getPrecio() + 25

class ServicioLimpieza(ServicioAdicional):
    def getDescripcion(self) -> str:
        return self.habitacion.getDescripcion() + " + Servicio Limpieza"

    def getPrecio(self) -> float:
        return self.habitacion.getPrecio() + 20
