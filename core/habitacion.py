"""
Módulo que define la clase base Habitacion.
"""

from core.ihabitacion import IHabitacion

class Habitacion(IHabitacion):
    """
    Representa una habitación genérica del hotel.

    Atributos:
        numero (int): Número identificador de la habitación.
        descripcion (str): Descripción de la habitación.
        precio_base (float): Precio base de la habitación.
        estado (EstadoHabitacion): Estado actual de la habitación.
    """

    def __init__(self, numero: int, descripcion: str, precio_base: float):
        """
        Inicializa una nueva habitación con su número, descripción y precio base.

        Args:
            numero (int): Número de la habitación.
            descripcion (str): Descripción de la habitación.
            precio_base (float): Precio base de la habitación.
        """
        self.numero = numero
        self.descripcion = descripcion
        self.precio_base = precio_base
        self.estado = None

    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado actual de la habitación.

        Args:
            nuevo_estado (EstadoHabitacion): Nuevo estado a aplicar.
        """
        self.estado = nuevo_estado
        self.estado.set_habitacion(self)

    def manejar_estado(self):
        """
        Invoca la lógica del estado actual, si existe.
        """
        if self.estado:
            self.estado.manejar_estado()

    def get_descripcion(self) -> str:
        """
        Retorna la descripción de la habitación.

        Returns:
            str: Descripción de la habitación.
        """
        return self.descripcion

    def get_precio(self) -> float:
        """
        Retorna el precio base de la habitación.

        Returns:
            float: Precio base.
        """
        return self.precio_base
