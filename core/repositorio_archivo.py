"""
Módulo que implementa un repositorio JSON para reservas y habitaciones.
"""

import json
import os
from datetime import datetime
from core.repositorio import IRepositorioReservas


class RepositorioArchivo(IRepositorioReservas):
    """
    Repositorio que almacena reservas y habitaciones en archivos JSON.
    """

    def __init__(self, archivo_reservas="reservas.json", archivo_habitaciones="habitaciones.json", archivo_precios="precios_tipos.json"):
        """
        Inicializa el repositorio con los archivos JSON especificados.

        Args:
            archivo_reservas (str): Ruta al archivo JSON de reservas.
            archivo_habitaciones (str): Ruta al archivo JSON de habitaciones.
            archivo_precios (str): Ruta al archivo JSON de precios por tipo.
        """
        self.archivo_reservas = archivo_reservas
        self.archivo_habitaciones = archivo_habitaciones
        self.archivo_precios = archivo_precios
        
        # Crear archivos vacíos si no existen
        self._inicializar_archivos()

    def _inicializar_archivos(self):
        """Crea los archivos JSON con estructuras vacías si no existen."""
        archivos_datos = [
            (self.archivo_reservas, []),
            (self.archivo_habitaciones, []),
            (self.archivo_precios, {})
        ]
        
        for archivo, estructura_inicial in archivos_datos:
            if not os.path.exists(archivo):
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(estructura_inicial, f, indent=2, ensure_ascii=False)

    def _leer_json(self, archivo):
        """
        Lee y parsea un archivo JSON.

        Args:
            archivo (str): Ruta al archivo JSON.

        Returns:
            object: Datos parseados del JSON.
        """
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si hay error, retornar estructura vacía apropiada
            if archivo == self.archivo_precios:
                return {}
            return []

    def _escribir_json(self, archivo, datos):
        """
        Escribe datos a un archivo JSON.

        Args:
            archivo (str): Ruta al archivo JSON.
            datos (object): Datos a escribir.
        """
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def guardar(self, reserva):
        """
        Guarda o actualiza una reserva en el archivo JSON.

        Args:
            reserva (object): Objeto reserva con los datos necesarios.
        """
        reservas = self._leer_json(self.archivo_reservas)
        
        # Convertir la reserva a diccionario
        reserva_dict = {
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
            "estado": reserva.estado,
            "fecha_creacion": datetime.now().isoformat()
        }
        
        # Buscar si la reserva ya existe para actualizarla
        indice_existente = None
        for i, r in enumerate(reservas):
            if r["id"] == reserva.id:
                indice_existente = i
                break
        
        if indice_existente is not None:
            reservas[indice_existente] = reserva_dict
        else:
            reservas.append(reserva_dict)
        
        self._escribir_json(self.archivo_reservas, reservas)

    def buscar_por_id(self, id_reserva):
        """
        Busca una reserva por su ID.

        Args:
            id_reserva (int): Identificador de la reserva.

        Returns:
            dict or None: Diccionario con los datos de la reserva o None si no se encuentra.
        """
        reservas = self._leer_json(self.archivo_reservas)
        
        for reserva in reservas:
            if reserva["id"] == id_reserva:
                return reserva
        
        return None

    def eliminar(self, id_reserva):
        """
        Elimina una reserva por su ID.

        Args:
            id_reserva (int): Identificador de la reserva.
        """
        reservas = self._leer_json(self.archivo_reservas)
        reservas_filtradas = [r for r in reservas if r["id"] != id_reserva]
        self._escribir_json(self.archivo_reservas, reservas_filtradas)

    def obtener_todas(self):
        """
        Obtiene todas las reservas almacenadas.

        Returns:
            list: Lista de reservas en formato dict.
        """
        return self._leer_json(self.archivo_reservas)

    def guardar_habitacion(self, habitacion):
        """
        Guarda o actualiza una habitación en el archivo JSON.

        Args:
            habitacion (object): Objeto habitación con los datos requeridos.
        """
        habitaciones = self._leer_json(self.archivo_habitaciones)
        
        # Determinar el tipo de habitación
        tipo = habitacion.__class__.__name__.replace('Habitacion', '').lower()
        if tipo == "estandar":
            tipo = "estandar"
        
        # Convertir la habitación a diccionario
        habitacion_dict = {
            "numero": habitacion.numero,
            "tipo": tipo,
            "descripcion": habitacion.get_descripcion(),
            "precio": habitacion.get_precio(),
            "estado": habitacion.estado.__class__.__name__ if habitacion.estado else "Disponible",
            "fecha_actualizacion": datetime.now().isoformat()
        }
        
        # Buscar si la habitación ya existe para actualizarla
        indice_existente = None
        for i, h in enumerate(habitaciones):
            if h["numero"] == habitacion.numero:
                indice_existente = i
                break
        
        if indice_existente is not None:
            habitaciones[indice_existente] = habitacion_dict
        else:
            habitaciones.append(habitacion_dict)
        
        self._escribir_json(self.archivo_habitaciones, habitaciones)

    def obtener_habitaciones(self):
        """
        Obtiene todas las habitaciones almacenadas.

        Returns:
            list: Lista de habitaciones en formato dict.
        """
        return self._leer_json(self.archivo_habitaciones)

    def actualizar_estado_habitacion(self, numero_habitacion, nuevo_estado):
        """
        Actualiza el estado de una habitación específica.

        Args:
            numero_habitacion (int): Número de la habitación.
            nuevo_estado (str): Nuevo estado a asignar.
        """
        habitaciones = self._leer_json(self.archivo_habitaciones)
        
        for habitacion in habitaciones:
            if habitacion["numero"] == numero_habitacion:
                habitacion["estado"] = nuevo_estado
                habitacion["fecha_actualizacion"] = datetime.now().isoformat()
                break
        
        self._escribir_json(self.archivo_habitaciones, habitaciones)

    def guardar_precio_tipo(self, tipo_habitacion: str, precio: float):
        """
        Guarda el precio base para un tipo de habitación.

        Args:
            tipo_habitacion (str): Tipo de habitación ('estandar', 'doble', 'suite').
            precio (float): Precio base para este tipo.
        """
        precios = self._leer_json(self.archivo_precios)
        precios[tipo_habitacion.lower()] = precio
        self._escribir_json(self.archivo_precios, precios)

    def obtener_precio_tipo(self, tipo_habitacion: str):
        """
        Obtiene el precio base para un tipo de habitación.

        Args:
            tipo_habitacion (str): Tipo de habitación.

        Returns:
            float or None: Precio base o None si no existe.
        """
        precios = self._leer_json(self.archivo_precios)
        return precios.get(tipo_habitacion.lower())

    def obtener_todos_precios_tipos(self):
        """
        Obtiene todos los precios por tipo de habitación.

        Returns:
            dict: Diccionario con tipos como clave y precios como valor.
        """
        return self._leer_json(self.archivo_precios)

    def migrar_desde_bd(self, repositorio_bd):
        """
        Migra todos los datos desde un repositorio de base de datos a archivos JSON.

        Args:
            repositorio_bd (RepositorioBD): Instancia del repositorio de base de datos.
        
        Returns:
            dict: Resumen de la migración realizada.
        """
        try:
            # Migrar reservas
            reservas_bd = repositorio_bd.obtener_todas()
            if reservas_bd:
                self._escribir_json(self.archivo_reservas, reservas_bd)
            
            # Migrar habitaciones
            habitaciones_bd = repositorio_bd.obtener_habitaciones()
            if habitaciones_bd:
                self._escribir_json(self.archivo_habitaciones, habitaciones_bd)
            
            # Migrar precios por tipo
            precios_bd = repositorio_bd.obtener_todos_precios_tipos()
            if precios_bd:
                self._escribir_json(self.archivo_precios, precios_bd)
            
            resumen = {
                "estado": "exitoso",
                "reservas_migradas": len(reservas_bd) if reservas_bd else 0,
                "habitaciones_migradas": len(habitaciones_bd) if habitaciones_bd else 0,
                "precios_migrados": len(precios_bd) if precios_bd else 0,
                "fecha_migracion": datetime.now().isoformat()
            }
            
            # Guardar log de migración
            with open("migracion_log.json", "w", encoding='utf-8') as f:
                json.dump(resumen, f, indent=2, ensure_ascii=False)
            
            return resumen
            
        except Exception as e:
            error_info = {
                "estado": "error",
                "mensaje": str(e),
                "fecha_error": datetime.now().isoformat()
            }
            
            with open("migracion_error.json", "w", encoding='utf-8') as f:
                json.dump(error_info, f, indent=2, ensure_ascii=False)
            
            return error_info

    def migrar_hacia_bd(self, repositorio_bd):
        """
        Migra todos los datos desde archivos JSON hacia un repositorio de base de datos.
        
        Args:
            repositorio_bd (RepositorioBD): Instancia del repositorio de base de datos.
        
        Returns:
            dict: Resumen de la migración realizada.
        """
        try:
            # Esta función requeriría recrear objetos desde los datos JSON
            # Por simplicidad, solo migramos los datos raw
            
            reservas_json = self._leer_json(self.archivo_reservas)
            habitaciones_json = self._leer_json(self.archivo_habitaciones)
            precios_json = self._leer_json(self.archivo_precios)
            
            # Migrar precios (esto es directo)
            for tipo, precio in precios_json.items():
                repositorio_bd.guardar_precio_tipo(tipo, precio)
            
            resumen = {
                "estado": "parcial",
                "mensaje": "Migración de precios completada. Reservas y habitaciones requieren objetos reconstituidos.",
                "precios_migrados": len(precios_json),
                "fecha_migracion": datetime.now().isoformat()
            }
            
            return resumen
            
        except Exception as e:
            return {
                "estado": "error",
                "mensaje": str(e),
                "fecha_error": datetime.now().isoformat()
            }

    def obtener_estadisticas(self):
        """
        Proporciona estadísticas sobre los datos almacenados.
        
        Returns:
            dict: Estadísticas del repositorio.
        """
        reservas = self._leer_json(self.archivo_reservas)
        habitaciones = self._leer_json(self.archivo_habitaciones)
        precios = self._leer_json(self.archivo_precios)
        
        # Estadísticas de habitaciones por tipo
        tipos_habitaciones = {}
        for habitacion in habitaciones:
            tipo = habitacion.get("tipo", "desconocido")
            tipos_habitaciones[tipo] = tipos_habitaciones.get(tipo, 0) + 1
        
        # Estadísticas de reservas por estado
        estados_reservas = {}
        for reserva in reservas:
            estado = reserva.get("estado", "desconocido")
            estados_reservas[estado] = estados_reservas.get(estado, 0) + 1
        
        return {
            "total_reservas": len(reservas),
            "total_habitaciones": len(habitaciones),
            "tipos_precios_configurados": len(precios),
            "habitaciones_por_tipo": tipos_habitaciones,
            "reservas_por_estado": estados_reservas,
            "archivos": {
                "reservas": self.archivo_reservas,
                "habitaciones": self.archivo_habitaciones,
                "precios": self.archivo_precios
            }
        }



def migrar_bd_a_json(ruta_bd="hotel.db", 
                     archivo_reservas="reservas.json", 
                     archivo_habitaciones="habitaciones.json", 
                     archivo_precios="precios_tipos.json"):
    """
    Función de utilidad para migrar datos de SQLite a JSON.
    """
    from core.repositorio_bd import RepositorioBD

    repo_bd = RepositorioBD(ruta_bd)
    repo_archivo = RepositorioArchivo(archivo_reservas, archivo_habitaciones, archivo_precios)
    resultado = repo_archivo.migrar_desde_bd(repo_bd)
    repo_bd.cerrar()
    return resultado
