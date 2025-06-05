import unittest
from datetime import date
from core.factura import Factura
from core.reserva import Reserva
from core.cliente import Cliente
from core.habitaciones_concretas import HabitacionEstandar
from core.servicios import ServicioRestaurante, ServicioLimpieza

class TestFactura(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("María", "987654321")
        self.habitacion = HabitacionEstandar(101)
        self.reserva = Reserva(
            id=1,
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_inicio=date.today(),
            fecha_fin=date.today(),
            estado="Ocupada"
        )

    def test_factura_basica(self):
        factura = Factura(self.reserva)
        contenido = factura.generar_factura()
        self.assertIn("María", contenido)
        self.assertIn("Habitación: 101", contenido)
        self.assertIn("Total a pagar", contenido)
        self.assertEqual(factura.total, self.habitacion.get_precio())

    def test_factura_con_servicios(self):
        self.reserva.agregar_servicio(ServicioRestaurante)
        self.reserva.agregar_servicio(ServicioLimpieza)
        factura = Factura(self.reserva)
        contenido = factura.generar_factura()
        self.assertIn("Restaurante", contenido)
        self.assertIn("Limpieza", contenido)
        total_esperado = self.habitacion.get_precio() + 30 + 20
        self.assertEqual(factura.total, total_esperado)

if __name__ == '__main__':
    unittest.main()
