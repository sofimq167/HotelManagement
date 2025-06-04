import unittest
import os
import tempfile
from core.reserva import Reserva
from core.cliente import Cliente
from core.habitaciones_concretas import HabitacionEstandar
from core.servicios import ServicioLimpieza
from core.repositorio_archivo import RepositorioArchivo
from datetime import date

class TestRepositorioArchivo(unittest.TestCase):
    def setUp(self):
        # Crear archivos temporales y cerrarlos de inmediato (clave en Windows)
        self.temp_reservas = tempfile.NamedTemporaryFile(delete=False)
        self.temp_reservas.close()

        self.temp_habitaciones = tempfile.NamedTemporaryFile(delete=False)
        self.temp_habitaciones.close()

        # Crear repositorio usando archivos temporales
        self.repo = RepositorioArchivo(
            ruta_reservas=self.temp_reservas.name,
            ruta_habitaciones=self.temp_habitaciones.name
        )

        # Cliente y habitación base
        self.cliente = Cliente("Laura", "111")
        self.habitacion = HabitacionEstandar(101)

    def tearDown(self):
        # Eliminar los archivos temporales
        os.unlink(self.temp_reservas.name)
        os.unlink(self.temp_habitaciones.name)

    def test_guardar_y_obtener_habitacion(self):
        self.repo.guardarHabitacion(self.habitacion)
        habitaciones = self.repo.obtenerHabitaciones()
        self.assertEqual(len(habitaciones), 1)
        self.assertEqual(habitaciones[0]["numero"], 101)

    def test_guardar_y_obtener_reserva(self):
        reserva = Reserva(1, self.cliente, self.habitacion, date.today(), date.today())
        reserva.agregar_servicio(ServicioLimpieza)
        self.repo.guardar(reserva)

        reservas = self.repo.obtenerTodas()
        self.assertEqual(len(reservas), 1)
        self.assertEqual(reservas[0]["id"], 1)
        self.assertEqual(reservas[0]["cliente"]["nombre"], "Laura")

    def test_eliminar_reserva(self):
        reserva = Reserva(2, self.cliente, self.habitacion, date.today(), date.today())
        self.repo.guardar(reserva)
        self.repo.eliminar(2)
        reservas = self.repo.obtenerTodas()
        self.assertEqual(len(reservas), 0)

if __name__ == '__main__':
    unittest.main()
