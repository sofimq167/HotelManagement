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
            fechaInicio=date.today(),
            fechaFin=date.today(),
            estado="Ocupada"
        )

    def test_factura_basica(self):
        factura = Factura(self.reserva)
        contenido = factura.generarFactura()
        self.assertIn("María", contenido)
        self.assertIn("Habitación: 101", contenido)
        self.assertIn("Total a pagar", contenido)
        self.assertEqual(factura.total, self.habitacion.getPrecio())

    def test_factura_con_servicios(self):
        self.reserva.agregar_servicio(ServicioRestaurante)
        self.reserva.agregar_servicio(ServicioLimpieza)
        factura = Factura(self.reserva)
        contenido = factura.generarFactura()
        self.assertIn("Restaurante", contenido)
        self.assertIn("Limpieza", contenido)
        total_esperado = self.habitacion.getPrecio() + 30 + 20
        self.assertEqual(factura.total, total_esperado)

if __name__ == '__main__':
    unittest.main()
