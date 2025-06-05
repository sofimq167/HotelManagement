"""Módulo que define la clase Reserva del sistema hotelero."""


class Reserva:
    """
    Representa una reserva realizada por un cliente.
    """

    def __init__(self, id: int, cliente, habitacion, fecha_inicio, fecha_fin, estado="Reservada"):
        """
        Inicializa una nueva reserva.

        Args:
            id (int): ID único.
            cliente (object): Cliente que realiza la reserva.
            habitacion (object): Habitación asociada.
            fecha_inicio (str/date): Fecha de entrada.
            fecha_fin (str/date): Fecha de salida.
            estado (str): Estado inicial (por defecto "Reservada").
        """
        self.id = id
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.servicios = []
        self.factura = None

    def agregar_servicio(self, servicio):
        """
        Agrega un servicio adicional a la habitación.

        Args:
            servicio (class): Clase del servicio (tipo Decorator).
        """
        self.habitacion = servicio(self.habitacion)
        self.servicios.append(servicio.__name__)

    def __str__(self) -> str:
        """
        Retorna una representación legible de la reserva.

        Returns:
            str: Representación de la reserva.
        """
        return (f"Reserva #{self.id} - Cliente: {self.cliente} - "
                f"Habitación: {self.habitacion.numero} - Estado: {self.estado}")
