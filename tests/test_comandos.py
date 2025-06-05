import unittest
from unittest.mock import Mock
from datetime import date
from core.cliente import Cliente
from core.habitaciones_concretas import HabitacionEstandar
from core.reserva_manager import ReservaManager
from core.crear_reserva_command import CrearReservaCommand
from core.registrar_checkin_command import RegistrarCheckInCommand
from core.registrar_checkout_command import RegistrarCheckOutCommand

class TestComandosReserva(unittest.TestCase):
    def setUp(self):
        # Reiniciar instancia singleton
        ReservaManager._instancia = None
        self.repositorio_mock = Mock()
        self.repositorio_mock.obtener_habitaciones.return_value = []
        self.repositorio_mock.obtener_todas.return_value = []

        self.manager = ReservaManager.getInstancia(self.repositorio_mock)
        self.cliente = Cliente("Pedro", "111")
        self.habitacion = HabitacionEstandar(101)
        self.manager.agregar_habitacion(self.habitacion)

    def test_crear_reserva_command(self):
        comando = CrearReservaCommand(
            self.cliente, self.habitacion, date.today(), date.today(), self.manager
        )
        reserva = comando.ejecutar()
        self.assertEqual(reserva.cliente.nombre, "Pedro")
        self.assertEqual(reserva.habitacion.numero, 101)
        self.assertEqual(reserva.estado, "Reservada")

    def test_registrar_checkin_command(self):
        comando_crear = CrearReservaCommand(
            self.cliente, self.habitacion, date.today(), date.today(), self.manager
        )
        reserva = comando_crear.ejecutar()

        comando_checkin = RegistrarCheckInCommand(reserva.id, self.manager)
        resultado = comando_checkin.ejecutar()
        self.assertTrue(resultado)

    def test_registrar_checkout_command(self):
        comando_crear = CrearReservaCommand(
            self.cliente, self.habitacion, date.today(), date.today(), self.manager
        )
        reserva = comando_crear.ejecutar()

        # Hacer check-in primero
        comando_checkin = RegistrarCheckInCommand(reserva.id, self.manager)
        comando_checkin.ejecutar()

        # Hacer check-out
        comando_checkout = RegistrarCheckOutCommand(reserva.id, self.manager)
        factura = comando_checkout.ejecutar()
        self.assertIsNotNone(factura)
        self.assertIn("FACTURA", factura.generar_factura())

if __name__ == '__main__':
    unittest.main()
