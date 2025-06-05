"""
Módulo que define la fábrica de habitaciones según el tipo solicitado.
"""

from core.habitaciones_concretas import HabitacionEstandar, HabitacionDoble, HabitacionSuite

class HabitacionFactory:
    """
    Fábrica para crear habitaciones según su tipo.

    Métodos:
        crear_habitacion(tipo, numero): Crea una instancia del tipo de habitación especificado.
    """
    def __init__(self, repositorio=None):
        self.repositorio = repositorio

    def crear_habitacion(self, tipo: str, numero: int):
        """
        Crea una habitación del tipo indicado.

        Args:
            tipo (str): Tipo de habitación ('estandar', 'doble' o 'suite').
            numero (int): Número identificador de la habitación.

        Returns:
            object: Instancia de la clase correspondiente al tipo de habitación.

        Raises:
            ValueError: Si el tipo de habitación no es válido.
        """
        tipo = tipo.lower()
        if tipo == "estandar":
            return HabitacionEstandar(numero, self.repositorio)
        if tipo == "doble":
            return HabitacionDoble(numero, self.repositorio)
        if tipo == "suite":
            return HabitacionSuite(numero, self.repositorio)

        raise ValueError(f"Tipo de habitación no válido: {tipo}")
 