from abc import ABC, abstractmethod

class EstadoHabitacion(ABC):
    def __init__(self):
        self.habitacion = None

    def setHabitacion(self, h):
        self.habitacion = h

    @abstractmethod
    def manejarEstado(self):
        pass
