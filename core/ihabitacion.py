"""
Módulo que define la interfaz IHabitacion.
"""

from abc import ABC, abstractmethod

class IHabitacion(ABC):
    """
    Interfaz para representar los métodos obligatorios de una habitación.
    """

    @abstractmethod
    def get_descripcion(self) -> str:
        """
        Retorna la descripción de la habitación.

        Returns:
            str: Descripción textual.
        """
        raise NotImplementedError("Debe implementar get_descripcion()")

    @abstractmethod
    def get_precio(self) -> float:
        """
        Retorna el precio de la habitación.

        Returns:
            float: Precio de la habitación.
        """
        raise NotImplementedError("Debe implementar get_precio()")
