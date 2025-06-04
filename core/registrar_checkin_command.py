from core.comando import Comando

class RegistrarCheckInCommand(Comando):
    def __init__(self, idReserva, receptor):
        self.idReserva = idReserva
        self.receptor = receptor

    def ejecutar(self):
        return self.receptor.checkin(self.idReserva)
