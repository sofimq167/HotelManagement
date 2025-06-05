"""
Módulo que implementa un repositorio de reservas y habitaciones en archivos JSON.
"""

import json
import os
from core.repositorio import IRepositorioReservas


class RepositorioArchivo(IRepositorioReservas):
    """
    Repositorio basado en archivos para gestionar reservas y habitaciones.
    """

    def __init__(self, ruta_reservas="reservas.json", ruta_habitaciones="habitaciones.json", ruta_precios="precios_tipos.json"):
        """
        Inicializa el repositorio con las rutas de archivo y crea archivos vacíos si no existen.
        """
        self.ruta_reservas = ruta_reservas
        self.ruta_habitaciones = ruta_habitaciones
        self.ruta_precios = ruta_precios

        # Inicializar archivos si no existen
        for ruta, contenido in [(self.ruta_reservas, []), (self.ruta_habitaciones, []), (self.ruta_precios, {})]:
            if not os.path.exists(ruta):
                with open(ruta, "w", encoding="utf-8") as archivo:
                    json.dump(contenido, archivo)

    def guardar(self, reserva):
        """
        Guarda o actualiza una reserva en el archivo.

        Args:
            reserva (object): Objeto reserva con los atributos necesarios.
        """
        reservas = self._leer_todas_reservas()

        # Verificar si la reserva ya existe
        reserva_existente = next((i for i, r in enumerate(reservas) if r["id"] == reserva.id), None)

        reserva_data = {
            "id": reserva.id,
            "cliente": {
                "nombre": reserva.cliente.nombre,
                "documento": reserva.cliente.documento
            },
            "habitacion": reserva.habitacion.numero,
            "descripcion": reserva.habitacion.get_descripcion(),
            "precio": reserva.habitacion.get_precio(),
            "fecha_inicio": str(reserva.fecha_inicio),
            "fecha_fin": str(reserva.fecha_fin),
            "estado": reserva.estado
        }

        if reserva_existente is not None:
            reservas[reserva_existente] = reserva_data
        else:
            reservas.append(reserva_data)

        self._escribir_todas_reservas(reservas)

    def buscar_por_id(self, id_reserva):
        """
        Busca una reserva por su ID.

        Args:
            id_reserva (int): Identificador de la reserva.

        Returns:
            dict or None: La reserva si existe, o None.
        """
        reservas = self._leer_todas_reservas()
        return next((r for r in reservas if r["id"] == id_reserva), None)

    def eliminar(self, id_reserva):
        """
        Elimina una reserva por ID.

        Args:
            id_reserva (int): Identificador de la reserva a eliminar.
        """
        reservas = [r for r in self._leer_todas_reservas() if r["id"] != id_reserva]
        self._escribir_todas_reservas(reservas)

    def obtener_todas(self):
        """
        Retorna todas las reservas almacenadas.

        Returns:
            list: Lista de reservas.
        """
        return self._leer_todas_reservas()

    def guardar_habitacion(self, habitacion):
        """
        Guarda o actualiza una habitación en el repositorio.

        Args:
            habitacion (object): Objeto habitación con atributos requeridos.
        """
        habitaciones = self._leer_todas_habitaciones()

        habitacion_existente = next((i for i, h in enumerate(habitaciones)
                                     if h["numero"] == habitacion.numero), None)

        tipo = habitacion.__class__.__name__.replace("Habitacion", "").lower()

        habitacion_data = {
            "numero": habitacion.numero,
            "tipo": tipo,
            "descripcion": habitacion.get_descripcion(),
            "precio": habitacion.get_precio(),
            "estado": habitacion.estado.__class__.__name__ if habitacion.estado else "Disponible"
        }

        if habitacion_existente is not None:
            habitaciones[habitacion_existente] = habitacion_data
        else:
            habitaciones.append(habitacion_data)

        self._escribir_todas_habitaciones(habitaciones)

    def obtener_habitaciones(self):
        """
        Retorna todas las habitaciones almacenadas.

        Returns:
            list: Lista de habitaciones.
        """
        return self._leer_todas_habitaciones()

    def actualizar_estado_habitacion(self, numero_habitacion, nuevo_estado):
        """
        Actualiza el estado de una habitación específica.

        Args:
            numero_habitacion (int): Número identificador de la habitación.
            nuevo_estado (str): Nuevo estado a asignar.
        """
        habitaciones = self._leer_todas_habitaciones()
        for habitacion in habitaciones:
            if habitacion["numero"] == numero_habitacion:
                habitacion["estado"] = nuevo_estado
                break
        self._escribir_todas_habitaciones(habitaciones)

    def _leer_todas_reservas(self):
        try:
            with open(self.ruta_reservas, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _escribir_todas_reservas(self, reservas):
        with open(self.ruta_reservas, "w", encoding="utf-8") as archivo:
            json.dump(reservas, archivo, indent=4)

    def _leer_todas_habitaciones(self):
        try:
            with open(self.ruta_habitaciones, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _escribir_todas_habitaciones(self, habitaciones):
        with open(self.ruta_habitaciones, "w", encoding="utf-8") as archivo:
            json.dump(habitaciones, archivo, indent=4)
    
    def guardar_precio_tipo(self, tipo_habitacion: str, precio: float):
        """Guarda el precio base para un tipo de habitación."""
        precios = self._leer_precios_tipos()
        precios[tipo_habitacion.lower()] = precio
        self._escribir_precios_tipos(precios)

    def obtener_precio_tipo(self, tipo_habitacion: str):
        """Obtiene el precio base para un tipo de habitación."""
        precios = self._leer_precios_tipos()
        return precios.get(tipo_habitacion.lower())

    def obtener_todos_precios_tipos(self):
        """Obtiene todos los precios por tipo de habitación."""
        return self._leer_precios_tipos()

    def _leer_precios_tipos(self):
        """Lee los precios desde el archivo JSON."""
        try:
            with open(self.ruta_precios, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _escribir_precios_tipos(self, precios):
        """Escribe los precios al archivo JSON."""
        with open(self.ruta_precios, "w", encoding="utf-8") as archivo:
            json.dump(precios, archivo, indent=4)