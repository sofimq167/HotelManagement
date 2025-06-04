from core.comando import Comando

class CrearReservaCommand(Comando):
    def __init__(self, cliente, habitacion, fechaInicio, fechaFin, receptor):
        self.cliente = cliente
        self.habitacion = habitacion
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.receptor = receptor

    def ejecutar(self):
        return self.receptor.crear_reserva(self.cliente, self.habitacion, self.fechaInicio, self.fechaFin)
