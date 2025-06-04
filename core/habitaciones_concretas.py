from core.habitacion import Habitacion

class HabitacionEstandar(Habitacion):
    def __init__(self, numero: int):
        super().__init__(numero, "Estándar Individual", 100.0)

class HabitacionDoble(Habitacion):
    def __init__(self, numero: int):
        super().__init__(numero, "Habitación Doble", 150.0)

class HabitacionSuite(Habitacion):
    def __init__(self, numero: int):
        super().__init__(numero, "Suite", 250.0)
