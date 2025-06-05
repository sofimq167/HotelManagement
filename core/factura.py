"""
Módulo que define la clase Factura para reservas hoteleras.
"""

class Factura:
    """
    Representa una factura generada a partir de una reserva.

    Atributos:
        reserva (object): La reserva asociada a la factura.
        descripcion (str): Descripción de la habitación.
        total (float): Costo total de la habitación.
        servicios (list): Lista de servicios adicionales.
    """

    def __init__(self, reserva):
        """
        Inicializa la factura a partir de una reserva.

        Args:
            reserva (object): Objeto reserva con cliente, habitación y fechas.
        """
        self.reserva = reserva
        self.descripcion = reserva.habitacion.get_descripcion()
        self.total = reserva.habitacion.get_precio()
        self.servicios = reserva.servicios if hasattr(reserva, 'servicios') else []

    def generar_factura(self):
        """
        Genera el contenido de la factura con información completa del cliente.

        Returns:
            str: Contenido formateado de la factura.
        """
        servicios_texto = (
            "\n".join(f"- {s}" for s in self.servicios) if self.servicios else "Ninguno"
        )

        
        info_cliente = self.reserva.cliente.get_info_completa()

        contenido = (
            f"{'='*50}\n"
            f"                FACTURA HOTEL\n"
            f"{'='*50}\n"
            f"Número de Reserva: {self.reserva.id}\n"
            f"Fecha de Emisión: {self._obtener_fecha_actual()}\n"
            f"\n"
            f"INFORMACIÓN DEL CLIENTE:\n"
            f"{'-'*30}\n"
            f"{info_cliente}\n"
            f"\n"
            f"DETALLES DE LA RESERVA:\n"
            f"{'-'*30}\n"
            f"Habitación: {self.reserva.habitacion.numero}\n"
            f"Descripción: {self.descripcion}\n"
            f"Fecha de ingreso: {self.reserva.fecha_inicio}\n"
            f"Fecha de salida: {self.reserva.fecha_fin}\n"
            f"Número de noches: {self._calcular_noches()}\n"
            f"\n"
            f"SERVICIOS ADICIONALES:\n"
            f"{'-'*30}\n"
            f"{servicios_texto}\n"
            f"\n"
            f"RESUMEN DE COSTOS:\n"
            f"{'-'*30}\n"
            f"Costo por noche: ${self._obtener_precio_base():.2f}\n"
            f"Número de noches: {self._calcular_noches()}\n"
            f"Subtotal habitación: ${self._calcular_subtotal_habitacion():.2f}\n"
            f"Servicios adicionales: ${self._calcular_costo_servicios():.2f}\n"
            f"TOTAL A PAGAR: ${self._calcular_subtotal_habitacion() + self._calcular_costo_servicios():.2f}\n"
            f"\n"
            f"Método de pago: {self.reserva.cliente.metodo_pago}\n"
            f"{'='*50}\n"
            f"¡Gracias por su preferencia!\n"
            f"{'='*50}"
        )

        print(contenido)
        self.guardar_en_archivo(contenido)
        return contenido

    def guardar_en_archivo(self, contenido):
        """
        Guarda el contenido de la factura en un archivo de texto.

        Args:
            contenido (str): Texto de la factura a guardar.
        """
        nombre_archivo = f"factura_{self.reserva.id}_{self.reserva.cliente.documento}.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)

    def _obtener_fecha_actual(self) -> str:
        """
        Obtiene la fecha actual formateada.

        Returns:
            str: Fecha actual en formato DD/MM/YYYY
        """
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y %H:%M")

    def _calcular_noches(self) -> int:
        """
        Calcula el número de noches de la reserva.

        Returns:
            int: Número de noches
        """
        return (self.reserva.fecha_fin - self.reserva.fecha_inicio).days

    def _obtener_precio_base(self) -> float:
        """
        Obtiene el precio base de la habitación sin servicios.

        Returns:
            float: Precio base por noche
        """
        # Si la habitación tiene decoradores (servicios), obtener el precio base
        habitacion = self.reserva.habitacion
        while hasattr(habitacion, 'habitacion'):
            habitacion = habitacion.habitacion
        return habitacion.get_precio()

    def _calcular_subtotal_habitacion(self) -> float:
        """
        Calcula el subtotal de la habitación sin servicios.

        Returns:
            float: Subtotal de la habitación
        """
        return self._obtener_precio_base() * self._calcular_noches()
    

    def _calcular_costo_servicios(self) -> float:
        """
        Calcula el costo de los servicios adicionales.

        Returns:
            float: Costo total de servicios adicionales
        """
        return self.total - self._obtener_precio_base()