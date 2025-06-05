# pylint: disable=too-few-public-methods
"""
Módulo que define los suscriptores del sistema de servicios para habitaciones.
"""

from core.observador import ISuscriptorServicio

class ModuloRestaurante(ISuscriptorServicio):
    """
    Módulo responsable de atender servicios de restaurante.
    """

    def notificar(self, habitacion, tipo_servicio):
        """
        Maneja la notificación de servicio de restaurante.

        Args:
            habitacion (object): Habitación que solicita el servicio.
            tipo_servicio (str): Tipo de servicio solicitado.
        """
        if tipo_servicio == "restaurante":
            print(f"[RESTAURANTE] Servicio solicitado en habitación {habitacion.numero}")


class ModuloLimpieza(ISuscriptorServicio):
    """
    Módulo responsable de atender servicios de limpieza.
    """

    def notificar(self, habitacion, tipo_servicio):
        """
        Maneja la notificación de servicio de limpieza.

        Args:
            habitacion (object): Habitación que solicita el servicio.
            tipo_servicio (str): Tipo de servicio solicitado.
        """
        if tipo_servicio in ["limpieza", "por_limpiar"]:
            print(f"[LIMPIEZA] Atención requerida en habitación {habitacion.numero}")


class ModuloAsistencia(ISuscriptorServicio):
    """
    Módulo responsable de atender servicios de asistencia.
    """

    def notificar(self, habitacion, tipo_servicio):
        """
        Maneja la notificación de servicio de asistencia.

        Args:
            habitacion (object): Habitación que solicita el servicio.
            tipo_servicio (str): Tipo de servicio solicitado.
        """
        if tipo_servicio == "asistencia":
            print(f"[ASISTENCIA] Servicio solicitado en habitación {habitacion.numero}")
