import unittest
from core.reserva_manager import ReservaManager
from core.reserva import Reserva
from core.servicios import ServicioRestaurante
from core.estado_disponible import Disponible 
from core.estado_ocupada import Ocupada
from unittest.mock import Mock
from datetime import date
from core.cliente import Cliente

class ReservaManagerTestCase(unittest.TestCase):
    def setUp(self):
        # Repositorio falso para evitar persistencia real
        self.repo_mock = Mock()
        self.repo_mock.obtener_habitaciones.return_value = []
        self.repo_mock.obtener_todas.return_value = []

        # Resetear la instancia singleton
        ReservaManager._instancia = None
        self.manager = ReservaManager.getInstancia(self.repo_mock)

        # Crear habitación manualmente
        from core.habitaciones_concretas import HabitacionEstandar
        self.habitacion = HabitacionEstandar(101)
        self.habitacion.cambiar_estado(Disponible())
        self.manager.agregar_habitacion(self.habitacion)

    def test_crear_reserva_exitosa(self):
        cliente = Cliente("Ana", "123")
        reserva = self.manager.crear_reserva(cliente, self.habitacion, date.today(), date.today())
        self.assertEqual(reserva.cliente.nombre, "Ana")
        self.assertEqual(reserva.estado, "Reservada")

    def test_checkin_id_invalido(self):
        result = self.manager.checkin(999)
        self.assertFalse(result)

    def test_checkout_sin_checkin(self):
        cliente = Cliente("Luis", "999")
        reserva = self.manager.crear_reserva(cliente, self.habitacion, date.today(), date.today())
        result = self.manager.checkout(reserva.id)
        self.assertIsNone(result)  # No debería permitir checkout sin checkin

    def test_agregar_servicio_a_reserva_ocupada(self):
        cliente = Cliente("Carlos", "888")
        reserva = self.manager.crear_reserva(cliente, self.habitacion, date.today(), date.today())
        self.manager.checkin(reserva.id)
        exito = self.manager.agregar_servicio_a_reserva(reserva.id, ServicioRestaurante)
        self.assertTrue(exito)
        self.assertIn("ServicioRestaurante", reserva.servicios)

    def test_agregar_servicio_a_reserva_finalizada(self):
        cliente = Cliente("Luisa", "777")
        reserva = self.manager.crear_reserva(cliente, self.habitacion, date.today(), date.today())
        self.manager.checkin(reserva.id)
        self.manager.checkout(reserva.id)
        resultado = self.manager.agregar_servicio_a_reserva(reserva.id, ServicioRestaurante)
        self.assertFalse(resultado)

if __name__ == '__main__':
    unittest.main()
