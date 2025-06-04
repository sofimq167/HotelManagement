from abc import ABC, abstractmethod

class ISuscriptorServicio(ABC):
    @abstractmethod
    def notificar(self, habitacion, tipo_servicio: str):
        pass


class NotificadorServicios:
    def __init__(self):
        self.suscriptores = []

    def suscribir(self, suscriptor: ISuscriptorServicio):
        if suscriptor not in self.suscriptores:
            self.suscriptores.append(suscriptor)

    def notificar_servicio(self, habitacion, tipo_servicio: str):
        for s in self.suscriptores:
            s.notificar(habitacion, tipo_servicio)
