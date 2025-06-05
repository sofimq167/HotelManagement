"""
Módulo que define los tipos concretos de habitaciones.
"""

from core.habitacion import Habitacion

class HabitacionEstandar(Habitacion):
    """
    Representa una habitación estándar individual.
    """
    def __init__(self, numero: int, repositorio=None):
        # Precios por defecto (fallback)
        precio_default = 100.0
        
        # Intentar obtener precio desde repositorio
        precio = precio_default
        if repositorio:
            precio_repo = repositorio.obtener_precio_tipo("estandar")
            if precio_repo is not None:
                precio = precio_repo
        
        super().__init__(numero, "Estándar Individual", precio)


class HabitacionDoble(Habitacion):
    """
    Representa una habitación doble.
    """
    def __init__(self, numero: int, repositorio=None):
        precio_default = 150.0
        
        precio = precio_default
        if repositorio:
            precio_repo = repositorio.obtener_precio_tipo("doble")
            if precio_repo is not None:
                precio = precio_repo
        
        super().__init__(numero, "Habitación Doble", precio)


class HabitacionSuite(Habitacion):
    """
    Representa una habitación tipo suite.
    """
    def __init__(self, numero: int, repositorio=None):
        precio_default = 250.0
        
        precio = precio_default
        if repositorio:
            precio_repo = repositorio.obtener_precio_tipo("suite")
            if precio_repo is not None:
                precio = precio_repo
        
        super().__init__(numero, "Suite", precio)