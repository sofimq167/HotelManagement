"""
Módulo que define la clase base abstracta para los estados de una habitación.
"""

from abc import ABC, abstractmethod

class EstadoHabitacion(ABC):
    """
    Clase abstracta base para representar el estado de una habitación.

    Métodos:
        set_habitacion(habitacion): Asocia una habitación al estado.
        manejar_estado(): Método abstracto para manejar la lógica del estado.
    """

    def __init__(self):
        """
        Inicializa el estado sin una habitación asociada.
        """
        self.habitacion = None

    def set_habitacion(self, habitacion):
        """
        Asocia una habitación a este estado.

        Args:
            habitacion (object): La habitación a la que se aplicará el estado.
        """
        self.habitacion = habitacion

    @abstractmethod
    def manejar_estado(self):
        """
        Maneja el comportamiento asociado al estado de la habitación.

        Este método debe ser implementado por cada subclase concreta.
        """
        raise NotImplementedError("Subclases deben implementar manejar_estado()")
