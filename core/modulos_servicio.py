from core.observador import ISuscriptorServicio

class ModuloRestaurante(ISuscriptorServicio):
    def notificar(self, habitacion, tipo_servicio):
        if tipo_servicio == "restaurante":
            print(f"[RESTAURANTE] Servicio solicitado en habitación {habitacion.numero}")

class ModuloLimpieza(ISuscriptorServicio):
    def notificar(self, habitacion, tipo_servicio):
        if tipo_servicio in ["limpieza", "por_limpiar"]:
            print(f"[LIMPIEZA] Atención requerida en habitación {habitacion.numero}")

class ModuloAsistencia(ISuscriptorServicio):
    def notificar(self, habitacion, tipo_servicio):
        if tipo_servicio == "asistencia":
            print(f"[ASISTENCIA] Servicio solicitado en habitación {habitacion.numero}")
