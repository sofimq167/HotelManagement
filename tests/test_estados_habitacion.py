import unittest
from core import estados_habitacion

# Simulación mínima de una habitación que usa setHabitacion en los estados
class HabitacionMock:
    def __init__(self):
        self.estado = estados_habitacion.Disponible()
        self.estado.setHabitacion(self)
        self.numero = 101  # Necesario para los prints

    def manejarEstado(self):
        self.estado.manejarEstado()

    def cambiarEstado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.estado.setHabitacion(self)  # Esto asegura que el nuevo estado tenga referencia a la habitación

class TestEstadosHabitacion(unittest.TestCase):

    def test_ciclo_de_estados(self):
        habitacion = HabitacionMock()
        self.assertEqual(habitacion.estado.__class__.__name__, "Disponible")

        habitacion.manejarEstado()
        self.assertEqual(habitacion.estado.__class__.__name__, "Reservada")

        habitacion.manejarEstado()
        self.assertEqual(habitacion.estado.__class__.__name__, "Ocupada")

        habitacion.manejarEstado()
        self.assertEqual(habitacion.estado.__class__.__name__, "PorLimpiar")

        habitacion.manejarEstado()
        self.assertEqual(habitacion.estado.__class__.__name__, "Disponible")

    def test_transiciones_individuales(self):
        habitacion = HabitacionMock()

        habitacion.estado = estados_habitacion.Reservada()
        habitacion.estado.setHabitacion(habitacion)
        habitacion.manejarEstado()
        self.assertIsInstance(habitacion.estado, estados_habitacion.Ocupada)

        habitacion.estado = estados_habitacion.Ocupada()
        habitacion.estado.setHabitacion(habitacion)
        habitacion.manejarEstado()
        self.assertIsInstance(habitacion.estado, estados_habitacion.PorLimpiar)

        habitacion.estado = estados_habitacion.PorLimpiar()
        habitacion.estado.setHabitacion(habitacion)
        habitacion.manejarEstado()
        self.assertIsInstance(habitacion.estado, estados_habitacion.Disponible)

if __name__ == '__main__':
    unittest.main()
