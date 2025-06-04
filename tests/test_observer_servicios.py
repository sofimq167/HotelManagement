import unittest
from core.habitaciones_concretas import HabitacionEstandar
from core.notificacion_global import notificador
from core.observador import ISuscriptorServicio

class RestauranteMock(ISuscriptorServicio):
    def __init__(self):
        self.notificado = False

    def notificar(self, habitacion, tipo_servicio):
        if tipo_servicio == "restaurante":
            self.notificado = True

class LimpiezaMock(ISuscriptorServicio):
    def __init__(self):
        self.notificado = False

    def notificar(self, habitacion, tipo_servicio):
        if tipo_servicio == "limpieza":
            self.notificado = True

class AsistenciaMock(ISuscriptorServicio):
    def __init__(self):
        self.notificado = False

    def notificar(self, habitacion, tipo_servicio):
        if tipo_servicio == "asistencia":
            self.notificado = True

class TestObserverServicios(unittest.TestCase):
    def setUp(self):
        self.habitacion = HabitacionEstandar(303)

        self.mock_restaurante = RestauranteMock()
        self.mock_limpieza = LimpiezaMock()
        self.mock_asistencia = AsistenciaMock()

        notificador.suscribir(self.mock_restaurante)
        notificador.suscribir(self.mock_limpieza)
        notificador.suscribir(self.mock_asistencia)

    def tearDown(self):
        notificador.suscriptores.remove(self.mock_restaurante)
        notificador.suscriptores.remove(self.mock_limpieza)
        notificador.suscriptores.remove(self.mock_asistencia)

    def test_notificacion_servicio_restaurante(self):
        notificador.notificar_servicio(self.habitacion, "restaurante")
        self.assertTrue(self.mock_restaurante.notificado)

    def test_notificacion_servicio_limpieza(self):
        notificador.notificar_servicio(self.habitacion, "limpieza")
        self.assertTrue(self.mock_limpieza.notificado)

    def test_notificacion_servicio_asistencia(self):
        notificador.notificar_servicio(self.habitacion, "asistencia")
        self.assertTrue(self.mock_asistencia.notificado)

if __name__ == "__main__":
    unittest.main()
