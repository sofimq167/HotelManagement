import json
import os
from core.repositorio import IRepositorioReservas

class RepositorioArchivo(IRepositorioReservas):
    def __init__(self, ruta_reservas="reservas.json", ruta_habitaciones="habitaciones.json"):
        self.ruta_reservas = ruta_reservas
        self.ruta_habitaciones = ruta_habitaciones
        
        # Inicializar archivo de reservas si no existe
        if not os.path.exists(self.ruta_reservas):
            with open(self.ruta_reservas, "w") as f:
                json.dump([], f)
        
        # Inicializar archivo de habitaciones si no existe
        if not os.path.exists(self.ruta_habitaciones):
            with open(self.ruta_habitaciones, "w") as f:
                json.dump([], f)

    def guardar(self, reserva):
        reservas = self._leer_todas_reservas()
        
        # Buscar si ya existe la reserva para actualizarla
        reserva_existente = None
        for i, r in enumerate(reservas):
            if r["id"] == reserva.id:
                reserva_existente = i
                break
        
        reserva_data = {
            "id": reserva.id,
            "cliente": {
                "nombre": reserva.cliente.nombre,
                "documento": reserva.cliente.documento
            },
            "habitacion": reserva.habitacion.numero,
            "descripcion": reserva.habitacion.getDescripcion(),
            "precio": reserva.habitacion.getPrecio(),
            "fechaInicio": str(reserva.fechaInicio),
            "fechaFin": str(reserva.fechaFin),
            "estado": reserva.estado
        }
        
        if reserva_existente is not None:
            reservas[reserva_existente] = reserva_data
        else:
            reservas.append(reserva_data)
            
        self._escribir_todas_reservas(reservas)

    def buscarPorId(self, id_reserva):
        reservas = self._leer_todas_reservas()
        for r in reservas:
            if r["id"] == id_reserva:
                return r
        return None

    def eliminar(self, id_reserva):
        reservas = self._leer_todas_reservas()
        reservas = [r for r in reservas if r["id"] != id_reserva]
        self._escribir_todas_reservas(reservas)
    
    def obtenerTodas(self):
        """Obtiene todas las reservas del repositorio"""
        return self._leer_todas_reservas()
    
    def guardarHabitacion(self, habitacion):
        """Guarda una habitación en el repositorio"""
        habitaciones = self._leer_todas_habitaciones()
        
        # Buscar si ya existe la habitación para actualizarla
        habitacion_existente = None
        for i, h in enumerate(habitaciones):
            if h["numero"] == habitacion.numero:
                habitacion_existente = i
                break
        
        # Determinar el tipo de habitación basado en su clase
        tipo = habitacion.__class__.__name__.replace('Habitacion', '').lower()
        if tipo == 'estandar':
            tipo = 'estandar'
        
        habitacion_data = {
            'numero': habitacion.numero,
            'tipo': tipo,
            'descripcion': habitacion.getDescripcion(),
            'precio': habitacion.getPrecio(),
            'estado': habitacion.estado.__class__.__name__ if habitacion.estado else 'Disponible'
        }
        
        if habitacion_existente is not None:
            habitaciones[habitacion_existente] = habitacion_data
        else:
            habitaciones.append(habitacion_data)
            
        self._escribir_todas_habitaciones(habitaciones)
    
    def obtenerHabitaciones(self):
        """Obtiene todas las habitaciones del repositorio"""
        return self._leer_todas_habitaciones()
    
    def actualizarEstadoHabitacion(self, numero_habitacion, nuevo_estado):
        """Actualiza el estado de una habitación específica"""
        habitaciones = self._leer_todas_habitaciones()
        
        for habitacion in habitaciones:
            if habitacion["numero"] == numero_habitacion:
                habitacion["estado"] = nuevo_estado
                break
        
        self._escribir_todas_habitaciones(habitaciones)

    def _leer_todas_reservas(self):
        try:
            with open(self.ruta_reservas, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _escribir_todas_reservas(self, reservas):
        with open(self.ruta_reservas, "w") as f:
            json.dump(reservas, f, indent=4)
    
    def _leer_todas_habitaciones(self):
        try:
            with open(self.ruta_habitaciones, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _escribir_todas_habitaciones(self, habitaciones):
        with open(self.ruta_habitaciones, "w") as f:
            json.dump(habitaciones, f, indent=4)