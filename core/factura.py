class Factura:
    def __init__(self, reserva):
        self.reserva = reserva
        self.descripcion = reserva.habitacion.getDescripcion()
        self.total = reserva.habitacion.getPrecio()
        self.servicios = reserva.servicios if hasattr(reserva, 'servicios') else []
    
    def generarFactura(self):
        servicios_texto = "\n".join(f"- {s}" for s in self.servicios) if self.servicios else "Ninguno"

        contenido = f"""
        ========== FACTURA ==========
        Cliente: {self.reserva.cliente}
        Habitación: {self.reserva.habitacion.numero}
        Descripción: {self.descripcion}
        Fecha de ingreso: {self.reserva.fechaInicio}
        Fecha de salida: {self.reserva.fechaFin}
        Servicios adicionales:
        {servicios_texto}
        Total a pagar: ${self.total:.2f}
        =============================
        """
        print(contenido)
        self.guardarEnArchivo(contenido)
        return contenido



    def guardarEnArchivo(self, contenido):
        with open(f"factura_{self.reserva.id}.txt", "w") as f:
            f.write(contenido)
