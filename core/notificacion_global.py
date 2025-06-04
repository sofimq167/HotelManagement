from core.observador import NotificadorServicios
from core.modulos_servicio import ModuloRestaurante, ModuloLimpieza, ModuloAsistencia

notificador = NotificadorServicios()

notificador.suscribir(ModuloRestaurante())
notificador.suscribir(ModuloLimpieza())
notificador.suscribir(ModuloAsistencia())
