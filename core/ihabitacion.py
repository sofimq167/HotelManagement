from abc import ABC, abstractmethod

class IHabitacion(ABC):
    @abstractmethod
    def getDescripcion(self) -> str:
        pass

    @abstractmethod
    def getPrecio(self) -> float:
        pass
