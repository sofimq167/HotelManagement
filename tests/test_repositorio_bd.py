import unittest
import os
from datetime import date
from core.repositorio_bd import RepositorioBD
from core.cliente import Cliente
from core.habitaciones_concretas import HabitacionEstandar
from core.reserva import Reserva

class TestRepositorioBD(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_hotel.db"
        self.repo = RepositorioBD(self.test_db_path)

        # Limpiar tablas antes de cada test
        self.repo.cursor.execute("DELETE FROM reservas")
        self.repo.cursor.execute("DELETE FROM habitaciones")
        self.repo.conn.commit()

        self.cliente = Cliente("Carlos", "444")
        self.habitacion = HabitacionEstandar(404)

    def tearDown(self):
        self.repo.cerrar()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_guardar_y_obtener_habitacion(self):
        self.repo.guardarHabitacion(self.habitacion)
        habitaciones = self.repo.obtenerHabitaciones()
        self.assertEqual(len(habitaciones), 1)
        self.assertEqual(habitaciones[0]['numero'], 404)

    def test_guardar_y_obtener_reserva(self):
        reserva = Reserva(1, self.cliente, self.habitacion, date.today(), date.today())
        self.repo.guardar(reserva)
        reservas = self.repo.obtenerTodas()
        self.assertEqual(len(reservas), 1)
        self.assertEqual(reservas[0]['cliente']['nombre'], "Carlos")

    def test_eliminar_reserva(self):
        reserva = Reserva(2, self.cliente, self.habitacion, date.today(), date.today())
        self.repo.guardar(reserva)
        self.repo.eliminar(2)
        reservas = self.repo.obtenerTodas()
        self.assertEqual(len(reservas), 0)

if __name__ == '__main__':
    unittest.main()
