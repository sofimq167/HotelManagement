from core.comando import Comando

class CancelarReservaCommand(Comando):
    def __init__(self, idReserva, receptor):
        self.idReserva = idReserva
        self.receptor = receptor

    def ejecutar(self):
        self.receptor.cancelar_reserva(self.idReserva)
