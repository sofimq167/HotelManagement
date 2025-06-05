import unittest
from core import estado_por_limpiar

# Simulación mínima de una habitación que usa set_habitacion en los estados
class HabitacionMock:
    def __init__(self):
        self.estado = estado_por_limpiar.Disponible()
        self.estado.set_habitacion(self)
        self.numero = 101  # Necesario para los prints

    def manejar_estado(self):
        self.estado.manejar_estado()

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.estado.set_habitacion(self)  # Esto asegura que el nuevo estado tenga referencia a la habitación

class TestEstadosHabitacion(unittest.TestCase):

    def test_ciclo_de_estados(self):
        habitacion = HabitacionMock()
        self.assertEqual(habitacion.estado.__class__.__name__, "Disponible")

        habitacion.manejar_estado()
        self.assertEqual(habitacion.estado.__class__.__name__, "Reservada")

        habitacion.manejar_estado()
        self.assertEqual(habitacion.estado.__class__.__name__, "Ocupada")

        habitacion.manejar_estado()
        self.assertEqual(habitacion.estado.__class__.__name__, "PorLimpiar")

        habitacion.manejar_estado()
        self.assertEqual(habitacion.estado.__class__.__name__, "Disponible")

    def test_transiciones_individuales(self):
        habitacion = HabitacionMock()

        habitacion.estado = estado_por_limpiar.Reservada()
        habitacion.estado.set_habitacion(habitacion)
        habitacion.manejar_estado()
        self.assertIsInstance(habitacion.estado, estado_por_limpiar.Ocupada)

        habitacion.estado = estado_por_limpiar.Ocupada()
        habitacion.estado.set_habitacion(habitacion)
        habitacion.manejar_estado()
        self.assertIsInstance(habitacion.estado, estado_por_limpiar.PorLimpiar)

        habitacion.estado = estado_por_limpiar.PorLimpiar()
        habitacion.estado.set_habitacion(habitacion)
        habitacion.manejar_estado()
        self.assertIsInstance(habitacion.estado, estado_por_limpiar.Disponible)

if __name__ == '__main__':
    unittest.main()
