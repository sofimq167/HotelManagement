from abc import ABC, abstractmethod

class IRepositorioReservas(ABC):
    @abstractmethod
    def guardar(self, reserva):
        pass

    @abstractmethod
    def buscarPorId(self, id_reserva: int):
        pass

    @abstractmethod
    def eliminar(self, id_reserva: int):
        pass
    
    @abstractmethod
    def obtenerTodas(self):
        """Obtiene todas las reservas del repositorio"""
        pass
    
    @abstractmethod
    def guardarHabitacion(self, habitacion):
        """Guarda una habitación en el repositorio"""
        pass
    
    @abstractmethod
    def obtenerHabitaciones(self):
        """Obtiene todas las habitaciones del repositorio"""
        pass
    
    @abstractmethod
    def actualizarEstadoHabitacion(self, numero_habitacion, nuevo_estado):
        """Actualiza el estado de una habitación específica"""
        pass