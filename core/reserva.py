class Reserva:
    def __init__(self, id: int, cliente, habitacion, fechaInicio, fechaFin, estado="Reservada"):
        self.id = id
        self.cliente = cliente
        self.habitacion = habitacion
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.estado = estado
        self.servicios = []
        self.factura = None
        
    def agregar_servicio(self, servicio):
        self.habitacion = servicio(self.habitacion)
        self.servicios.append(servicio.__name__)

    def __str__(self):
        return f"Reserva #{self.id} - Cliente: {self.cliente} - Habitación: {self.habitacion.numero} - Estado: {self.estado}"
