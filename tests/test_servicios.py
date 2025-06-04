import unittest
from core.servicios import ServicioRestaurante, ServicioLimpieza, ServicioAsistencia
from core.habitaciones_concretas import HabitacionEstandar

class TestServiciosAdicionales(unittest.TestCase):
    def setUp(self):
        self.habitacion_base = HabitacionEstandar(101)

    def test_servicio_restaurante(self):
        decorada = ServicioRestaurante(self.habitacion_base)
        self.assertIn("Restaurante", decorada.getDescripcion())
        self.assertEqual(decorada.getPrecio(), self.habitacion_base.getPrecio() + 30)

    def test_servicio_limpieza(self):
        decorada = ServicioLimpieza(self.habitacion_base)
        self.assertIn("Limpieza", decorada.getDescripcion())
        self.assertEqual(decorada.getPrecio(), self.habitacion_base.getPrecio() + 20)

    def test_servicio_asistencia(self):
        decorada = ServicioAsistencia(self.habitacion_base)
        self.assertIn("Asistencia", decorada.getDescripcion())
        self.assertEqual(decorada.getPrecio(), self.habitacion_base.getPrecio() + 25)

    def test_servicios_combinados(self):
        decorada = ServicioRestaurante(
                        ServicioLimpieza(
                            ServicioAsistencia(self.habitacion_base)))
        descripcion = decorada.getDescripcion()
        self.assertIn("Restaurante", descripcion)
        self.assertIn("Limpieza", descripcion)
        self.assertIn("Asistencia", descripcion)
        self.assertEqual(decorada.getPrecio(), self.habitacion_base.getPrecio() + 30 + 20 + 25)

if __name__ == '__main__':
    unittest.main()
