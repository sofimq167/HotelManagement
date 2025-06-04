import sqlite3
from core.repositorio import IRepositorioReservas

class RepositorioBD(IRepositorioReservas):
    def __init__(self, db_path="hotel.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._crear_tablas_si_no_existen()

    def _crear_tablas_si_no_existen(self):
        # Tabla de reservas
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
        
        # Tabla de habitaciones
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitaciones (
                numero INTEGER PRIMARY KEY,
                tipo TEXT,
                descripcion TEXT,
                precio REAL,
                estado TEXT
            )
        """)
        
        self.conn.commit()

    def guardar(self, reserva):
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
            reserva.habitacion.getDescripcion(),
            reserva.habitacion.getPrecio(),
            str(reserva.fechaInicio),
            str(reserva.fechaFin),
            reserva.estado
        ))
        self.conn.commit()

    def buscarPorId(self, id_reserva):
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
                "fechaInicio": resultado[6],
                "fechaFin": resultado[7],
                "estado": resultado[8]
            }
        return None

    def eliminar(self, id_reserva):
        self.cursor.execute("DELETE FROM reservas WHERE id = ?", (id_reserva,))
        self.conn.commit()
    
    def obtenerTodas(self):
        """Obtiene todas las reservas del repositorio"""
        self.cursor.execute("SELECT * FROM reservas")
        resultados = self.cursor.fetchall()
        
        reservas = []
        for resultado in resultados:
            reservas.append({
                "id": resultado[0],
                "cliente": {
                    "nombre": resultado[1],
                    "documento": resultado[2]
                },
                "habitacion": resultado[3],
                "descripcion": resultado[4],
                "precio": resultado[5],
                "fechaInicio": resultado[6],
                "fechaFin": resultado[7],
                "estado": resultado[8]
            })
        
        return reservas
    
    def guardarHabitacion(self, habitacion):
        """Guarda una habitación en el repositorio"""
        # Determinar el tipo de habitación basado en su clase
        tipo = habitacion.__class__.__name__.replace('Habitacion', '').lower()
        if tipo == 'estandar':
            tipo = 'estandar'
        
        self.cursor.execute("""
            INSERT OR REPLACE INTO habitaciones (
                numero, tipo, descripcion, precio, estado
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            habitacion.numero,
            tipo,
            habitacion.getDescripcion(),
            habitacion.getPrecio(),
            habitacion.estado.__class__.__name__ if habitacion.estado else 'Disponible'
        ))
        self.conn.commit()
    
    def obtenerHabitaciones(self):
        """Obtiene todas las habitaciones del repositorio"""
        self.cursor.execute("SELECT * FROM habitaciones")
        resultados = self.cursor.fetchall()
        
        habitaciones = []
        for resultado in resultados:
            habitaciones.append({
                'numero': resultado[0],
                'tipo': resultado[1],
                'descripcion': resultado[2],
                'precio': resultado[3],
                'estado': resultado[4]
            })
        
        return habitaciones
    
    def actualizarEstadoHabitacion(self, numero_habitacion, nuevo_estado):
        """Actualiza el estado de una habitación específica"""
        self.cursor.execute("""
            UPDATE habitaciones 
            SET estado = ? 
            WHERE numero = ?
        """, (nuevo_estado, numero_habitacion))
        self.conn.commit()

    def cerrar(self):
        if self.conn:
            self.conn.close()

    def __del__(self):
        try:
            self.cerrar()
        except:
            pass