import unittest
from core.servicios import ServicioRestaurante, ServicioLimpieza, ServicioAsistencia
from core.habitaciones_concretas import HabitacionEstandar

class TestServiciosAdicionales(unittest.TestCase):
    def setUp(self):
        self.habitacion_base = HabitacionEstandar(101)

    def test_servicio_restaurante(self):
        decorada = ServicioRestaurante(self.habitacion_base)
        self.assertIn("Restaurante", decorada.get_descripcion())
        self.assertEqual(decorada.get_precio(), self.habitacion_base.get_precio() + 30)

    def test_servicio_limpieza(self):
        decorada = ServicioLimpieza(self.habitacion_base)
        self.assertIn("Limpieza", decorada.get_descripcion())
        self.assertEqual(decorada.get_precio(), self.habitacion_base.get_precio() + 20)

    def test_servicio_asistencia(self):
        decorada = ServicioAsistencia(self.habitacion_base)
        self.assertIn("Asistencia", decorada.get_descripcion())
        self.assertEqual(decorada.get_precio(), self.habitacion_base.get_precio() + 25)

    def test_servicios_combinados(self):
        decorada = ServicioRestaurante(
                        ServicioLimpieza(
                            ServicioAsistencia(self.habitacion_base)))
        descripcion = decorada.get_descripcion()
        self.assertIn("Restaurante", descripcion)
        self.assertIn("Limpieza", descripcion)
        self.assertIn("Asistencia", descripcion)
        self.assertEqual(decorada.get_precio(), self.habitacion_base.get_precio() + 30 + 20 + 25)

if __name__ == '__main__':
    unittest.main()
