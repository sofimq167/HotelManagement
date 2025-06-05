"""Módulo que implementa un repositorio SQLite para reservas y habitaciones."""

import sqlite3
from core.repositorio import IRepositorioReservas


class RepositorioBD(IRepositorioReservas):
    """
    Repositorio que almacena reservas y habitaciones en una base de datos SQLite.
    """

    def __init__(self, db_path="hotel.db"):
        """
        Inicializa el repositorio y crea las tablas si no existen.

        Args:
            db_path (str): Ruta al archivo de base de datos SQLite.
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._crear_tablas_si_no_existen()

    def _crear_tablas_si_no_existen(self):
        """Crea las tablas de reservas y habitaciones si aún no existen."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY,
                cliente_nombre TEXT,
                cliente_documento TEXT,
                habitacion_numero INTEGER,
                descripcion TEXT,
                precio REAL,
                fecha_inicio TEXT,
                fecha_fin TEXT,
                estado TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitaciones (
                numero INTEGER PRIMARY KEY,
                tipo TEXT,
                descripcion TEXT,
                precio REAL,
                estado TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS precios_tipos (
                tipo TEXT PRIMARY KEY,
                precio REAL
            )
        """)

        self.conn.commit()

    def guardar(self, reserva):
        """
        Guarda o actualiza una reserva en la base de datos.

        Args:
            reserva (object): Objeto reserva con los datos necesarios.
        """
        self.cursor.execute("""
            INSERT OR REPLACE INTO reservas (
                id, cliente_nombre, cliente_documento,
                habitacion_numero, descripcion, precio,
                fecha_inicio, fecha_fin, estado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            reserva.id,
            reserva.cliente.nombre,
            reserva.cliente.documento,
            reserva.habitacion.numero,
            reserva.habitacion.get_descripcion(),
            reserva.habitacion.get_precio(),
            str(reserva.fecha_inicio),
            str(reserva.fecha_fin),
            reserva.estado
        ))
        self.conn.commit()

    def buscar_por_id(self, id_reserva):
        """
        Busca una reserva por su ID.

        Args:
            id_reserva (int): Identificador de la reserva.

        Returns:
            dict or None: Diccionario con los datos de la reserva o None si no se encuentra.
        """
        self.cursor.execute("SELECT * FROM reservas WHERE id = ?", (id_reserva,))
        resultado = self.cursor.fetchone()

        if resultado:
            return {
                "id": resultado[0],
                "cliente": {
                    "nombre": resultado[1],
                    "documento": resultado[2]
                },
                "habitacion": resultado[3],
                "descripcion": resultado[4],
                "precio": resultado[5],
                "fecha_inicio": resultado[6],
                "fecha_fin": resultado[7],
                "estado": resultado[8]
            }

        return None

    def eliminar(self, id_reserva):
        """
        Elimina una reserva por su ID.

        Args:
            id_reserva (int): Identificador de la reserva.
        """
        self.cursor.execute("DELETE FROM reservas WHERE id = ?", (id_reserva,))
        self.conn.commit()

    def obtener_todas(self):
        """
        Obtiene todas las reservas almacenadas.

        Returns:
            list: Lista de reservas en formato dict.
        """
        self.cursor.execute("SELECT * FROM reservas")
        resultados = self.cursor.fetchall()

        reservas = []
        for r in resultados:
            reservas.append({
                "id": r[0],
                "cliente": {
                    "nombre": r[1],
                    "documento": r[2]
                },
                "habitacion": r[3],
                "descripcion": r[4],
                "precio": r[5],
                "fecha_inicio": r[6],
                "fecha_fin": r[7],
                "estado": r[8]
            })

        return reservas

    def guardar_habitacion(self, habitacion):
        """
        Guarda o actualiza una habitación en la base de datos.

        Args:
            habitacion (object): Objeto habitación con los datos requeridos.
        """
        tipo = habitacion.__class__.__name__.replace('Habitacion', '').lower()
        if tipo == "estandar":
            tipo = "estandar"

        self.cursor.execute("""
            INSERT OR REPLACE INTO habitaciones (
                numero, tipo, descripcion, precio, estado
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            habitacion.numero,
            tipo,
            habitacion.get_descripcion(),
            habitacion.get_precio(),
            habitacion.estado.__class__.__name__ if habitacion.estado else "Disponible"
        ))
        self.conn.commit()

    def obtener_habitaciones(self):
        """
        Obtiene todas las habitaciones almacenadas.

        Returns:
            list: Lista de habitaciones en formato dict.
        """
        self.cursor.execute("SELECT * FROM habitaciones")
        resultados = self.cursor.fetchall()

        habitaciones = []
        for h in resultados:
            habitaciones.append({
                "numero": h[0],
                "tipo": h[1],
                "descripcion": h[2],
                "precio": h[3],
                "estado": h[4]
            })

        return habitaciones

    def actualizar_estado_habitacion(self, numero_habitacion, nuevo_estado):
        """
        Actualiza el estado de una habitación específica.

        Args:
            numero_habitacion (int): Número de la habitación.
            nuevo_estado (str): Nuevo estado a asignar.
        """
        self.cursor.execute("""
            UPDATE habitaciones
            SET estado = ?
            WHERE numero = ?
        """, (nuevo_estado, numero_habitacion))
        self.conn.commit()

    def cerrar(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.conn:
            self.conn.close()

    def __del__(self):
        """Destructor que garantiza el cierre de la conexión."""
        try:
            self.cerrar()
        except Exception:
            pass
    
    def guardar_precio_tipo(self, tipo_habitacion: str, precio: float):
        """Guarda el precio base para un tipo de habitación."""
        self.cursor.execute("""
            INSERT OR REPLACE INTO precios_tipos (tipo, precio)
            VALUES (?, ?)
        """, (tipo_habitacion.lower(), precio))
        self.conn.commit()

    def obtener_precio_tipo(self, tipo_habitacion: str):
        """Obtiene el precio base para un tipo de habitación."""
        self.cursor.execute(
            "SELECT precio FROM precios_tipos WHERE tipo = ?", 
            (tipo_habitacion.lower(),)
        )
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else None

    def obtener_todos_precios_tipos(self):
        """Obtiene todos los precios por tipo de habitación."""
        self.cursor.execute("SELECT tipo, precio FROM precios_tipos")
        resultados = self.cursor.fetchall()
        return {tipo: precio for tipo, precio in resultados}
