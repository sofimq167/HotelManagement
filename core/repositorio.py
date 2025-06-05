"""Módulo que define la interfaz para un repositorio de reservas y habitaciones."""

from abc import ABC, abstractmethod


class IRepositorioReservas(ABC):
    """
    Interfaz para el repositorio de reservas y habitaciones.
    Define las operaciones básicas que debe implementar cualquier repositorio concreto.
    """

    @abstractmethod
    def guardar(self, reserva):
        """
        Guarda una reserva en el repositorio.

        Args:
            reserva (object): Objeto que representa una reserva.
        """
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, id_reserva: int):
        """
        Busca una reserva por su ID.

        Args:
            id_reserva (int): Identificador de la reserva.

        Returns:
            object: Reserva encontrada o None.
        """
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, id_reserva: int):
        """
        Elimina una reserva por su ID.

        Args:
            id_reserva (int): Identificador de la reserva a eliminar.
        """
        raise NotImplementedError

    @abstractmethod
    def obtener_todas(self):
        """
        Obtiene todas las reservas del repositorio.

        Returns:
            list: Lista de reservas.
        """
        raise NotImplementedError

    @abstractmethod
    def guardar_habitacion(self, habitacion):
        """
        Guarda una habitación en el repositorio.

        Args:
            habitacion (object): Objeto que representa una habitación.
        """
        raise NotImplementedError

    @abstractmethod
    def obtener_habitaciones(self):
        """
        Obtiene todas las habitaciones del repositorio.

        Returns:
            list: Lista de habitaciones.
        """
        raise NotImplementedError

    @abstractmethod
    def actualizar_estado_habitacion(self, numero_habitacion, nuevo_estado):
        """
        Actualiza el estado de una habitación específica.

        Args:
            numero_habitacion (int): Número identificador de la habitación.
            nuevo_estado (str): Estado nuevo a asignar.
        """
        raise NotImplementedError
    
    @abstractmethod
    def guardar_precio_tipo(self, tipo_habitacion: str, precio: float):
        """
        Guarda el precio base para un tipo de habitación.

        Args:
            tipo_habitacion (str): Tipo de habitación ('estandar', 'doble', 'suite').
            precio (float): Precio base para este tipo.
        """
        raise NotImplementedError

    @abstractmethod
    def obtener_precio_tipo(self, tipo_habitacion: str):
        """
        Obtiene el precio base para un tipo de habitación.

        Args:
            tipo_habitacion (str): Tipo de habitación.

        Returns:
            float or None: Precio base o None si no existe.
        """
        raise NotImplementedError

    @abstractmethod
    def obtener_todos_precios_tipos(self):
        """
        Obtiene todos los precios por tipo de habitación.

        Returns:
            dict: Diccionario con tipos como clave y precios como valor.
        """
        raise NotImplementedError
