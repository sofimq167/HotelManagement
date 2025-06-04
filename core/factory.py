from core.habitaciones_concretas import HabitacionEstandar, HabitacionDoble, HabitacionSuite

class HabitacionFactory:
    def crearHabitacion(self, tipo: str, numero: int):
        tipo = tipo.lower()
        if tipo == "estandar":
            return HabitacionEstandar(numero)
        elif tipo == "doble":
            return HabitacionDoble(numero)
        elif tipo == "suite":
            return HabitacionSuite(numero)
        else:
            raise ValueError(f"Tipo de habitación no válido: {tipo}")
