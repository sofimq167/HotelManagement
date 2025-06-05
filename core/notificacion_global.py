"""
Módulo principal que configura los suscriptores de servicios para habitaciones.
"""

from core.observador import NotificadorServicios
from core.modulos_servicio import ModuloRestaurante, ModuloLimpieza, ModuloAsistencia

# Instancia única del notificador global
notificador = NotificadorServicios()

# Registro de módulos como suscriptores del sistema de notificaciones
notificador.suscribir(ModuloRestaurante())
notificador.suscribir(ModuloLimpieza())
notificador.suscribir(ModuloAsistencia())
