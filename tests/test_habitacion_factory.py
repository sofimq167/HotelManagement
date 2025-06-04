import unittest
from core.habitaciones_concretas import HabitacionEstandar, HabitacionDoble, HabitacionSuite
from core.factory import HabitacionFactory

class TestHabitacionFactory(unittest.TestCase):
    def setUp(self):
        self.factory = HabitacionFactory()

    def test_crear_habitacion_estandar(self):
        habitacion = self.factory.crearHabitacion("estandar", 101)
        self.assertIsInstance(habitacion, HabitacionEstandar)
        self.assertEqual(habitacion.numero, 101)
        self.assertGreater(habitacion.getPrecio(), 0)
        self.assertIn("Estándar", habitacion.getDescripcion())

    def test_crear_habitacion_doble(self):
        habitacion = self.factory.crearHabitacion("doble", 202)
        self.assertIsInstance(habitacion, HabitacionDoble)
        self.assertEqual(habitacion.numero, 202)
        self.assertIn("Doble", habitacion.getDescripcion())

    def test_crear_habitacion_suite(self):
        habitacion = self.factory.crearHabitacion("suite", 303)
        self.assertIsInstance(habitacion, HabitacionSuite)
        self.assertEqual(habitacion.numero, 303)
        self.assertIn("Suite", habitacion.getDescripcion())

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            self.factory.crearHabitacion("penthouse", 999)

if __name__ == '__main__':
    unittest.main()
