"""
Módulo que define los servicios adicionales aplicables a una habitación.
"""

from abc import ABC
from core.ihabitacion import IHabitacion


class ServicioAdicional(IHabitacion, ABC):
    """
    Clase base abstracta para servicios adicionales (patrón Decorator).
    """

    def __init__(self, habitacion: IHabitacion):
        """
        Inicializa el decorador con una habitación existente.

        Args:
            habitacion (IHabitacion): Habitación a decorar.
        """
        self.habitacion = habitacion

    def get_descripcion(self) -> str:
        """
        Devuelve la descripción extendida de la habitación.
        """
        return self.habitacion.get_descripcion()

    def get_precio(self) -> float:
        """
        Devuelve el precio total incluyendo el servicio adicional.
        """
        return self.habitacion.get_precio()
    
    def __getattr__(self,name):
        return getattr(self.habitacion, name)

    @property
    def numero(self):
        """
        Propiedad para acceder al número de habitación.
        """
        return self.habitacion.numero

    @property
    def descripcion_original(self):
        """
        Propiedad para acceder a la descripción base sin servicios.
        """
        return self.habitacion.descripcion

    @property
    def precio_base(self):
        """
        Propiedad para acceder al precio base sin servicios.
        """
        return self.habitacion.precio_base


class ServicioRestaurante(ServicioAdicional):
    """
    Servicio adicional de restaurante (+ $30).
    """

    def get_descripcion(self) -> str:
        return super().get_descripcion() + " + Servicio Restaurante"

    def get_precio(self) -> float:
        return super().get_precio() + 30


class ServicioAsistencia(ServicioAdicional):
    """
    Servicio adicional de asistencia (+ $25).
    """

    def get_descripcion(self) -> str:
        return super().get_descripcion() + " + Servicio Asistencia"

    def get_precio(self) -> float:
        return super().get_precio() + 25


class ServicioLimpieza(ServicioAdicional):
    """
    Servicio adicional de limpieza (+ $20).
    """

    def get_descripcion(self) -> str:
        return super().get_descripcion() + " + Servicio Limpieza"

    def get_precio(self) -> float:
        return super().get_precio() + 20
