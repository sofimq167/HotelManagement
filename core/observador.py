"""
Módulo que implementa el patrón Observer para servicios en habitaciones.
"""

from abc import ABC, abstractmethod


class ISuscriptorServicio(ABC):
    """
    Interfaz que define el comportamiento de los módulos suscriptores a servicios.
    """

    @abstractmethod
    def notificar(self, habitacion, tipo_servicio: str):
        """
        Recibe la notificación de un servicio solicitado.

        Args:
            habitacion (object): La habitación que solicita el servicio.
            tipo_servicio (str): Tipo de servicio solicitado (ej. 'limpieza').
        """
        raise NotImplementedError("Debe implementar el método notificar().")


class NotificadorServicios:
    """
    Clase que gestiona la suscripción y notificación de servicios a los módulos correspondientes.
    """

    def __init__(self):
        """Inicializa la lista de suscriptores."""
        self.suscriptores = []

    def suscribir(self, suscriptor: ISuscriptorServicio):
        """
        Registra un módulo como suscriptor.

        Args:
            suscriptor (ISuscriptorServicio): Módulo que implementa la interfaz de suscripción.
        """
        if suscriptor not in self.suscriptores:
            self.suscriptores.append(suscriptor)

    def notificar_servicio(self, habitacion, tipo_servicio: str):
        """
        Notifica a todos los módulos suscritos del tipo de servicio solicitado.

        Args:
            habitacion (object): Habitación que solicita el servicio.
            tipo_servicio (str): Tipo de servicio (ej. 'asistencia', 'limpieza').
        """
        for suscriptor in self.suscriptores:
            suscriptor.notificar(habitacion, tipo_servicio)
