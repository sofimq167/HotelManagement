from core.repositorio import IRepositorioReservas
from core.reserva import Reserva
from core.factura import Factura
from core.estados_habitacion import Disponible, Reservada, Ocupada, PorLimpiar
from datetime import datetime

class ReservaManager:
    _instancia = None

    def __init__(self, repositorio: IRepositorioReservas):
        self.repositorio = repositorio
        self.habitaciones = []  # Array de instancias de habitaciones
        self.reservas = []
        self._cargar_datos_iniciales()

    @classmethod
    def getInstancia(cls, repositorio=None):
        if cls._instancia is None:
            if repositorio is None:
                raise ValueError("Debe proporcionar un repositorio la primera vez.")
            cls._instancia = cls(repositorio)
        return cls._instancia

    def _cargar_datos_iniciales(self):
        """Carga habitaciones y reservas desde el repositorio al instanciarse"""
        # Cargar habitaciones desde el repositorio
        self._cargar_habitaciones_desde_repositorio()
        
        # Cargar reservas existentes desde el repositorio
        self._cargar_reservas_desde_repositorio()

    def _cargar_habitaciones_desde_repositorio(self):
        """Carga las habitaciones desde el repositorio"""
        try:
            datos_habitaciones = self.repositorio.obtenerHabitaciones()
            
            if not datos_habitaciones:
                # Si no hay habitaciones en el repositorio, crear habitaciones por defecto
                self._crear_habitaciones_por_defecto()
                return
            
            from core.factory import HabitacionFactory
            factory = HabitacionFactory()
            
            for datos in datos_habitaciones:
                habitacion = factory.crearHabitacion(datos['tipo'], datos['numero'])
                
                # Restaurar el estado de la habitación
                estado_clase = self._obtener_clase_estado(datos.get('estado', 'Disponible'))
                estado = estado_clase()
                habitacion.cambiarEstado(estado)
                
                self.habitaciones.append(habitacion)
                
        except Exception as e:
            print(f"Error cargando habitaciones desde repositorio: {e}")
            # Si hay error, inicializar con habitaciones por defecto
            self._crear_habitaciones_por_defecto()

    def _crear_habitaciones_por_defecto(self):
        """Crea habitaciones por defecto si no existen en el repositorio"""
        from core.factory import HabitacionFactory
        factory = HabitacionFactory()
        
        # Crear algunas habitaciones de ejemplo
        tipos_habitaciones = [
            ("estandar", 101), ("estandar", 102),
            ("doble", 201), ("doble", 202),
            ("suite", 301)
        ]
        
        for tipo, numero in tipos_habitaciones:
            habitacion = factory.crearHabitacion(tipo, numero)
            # Asignar estado inicial: Disponible
            estado = Disponible()
            habitacion.cambiarEstado(estado)
            
            self.habitaciones.append(habitacion)
            # Guardar en repositorio
            self.repositorio.guardarHabitacion(habitacion)

    def _cargar_reservas_desde_repositorio(self):
        """Carga reservas existentes desde el repositorio"""
        try:
            datos_reservas = self.repositorio.obtenerTodas()
            for datos in datos_reservas:
                cliente = type('Cliente', (), datos["cliente"])()  # cliente.nombre, cliente.documento
                habitacion = self.buscar_habitacion_por_id(datos["habitacion"])
                if habitacion:
                    reserva = Reserva(
                        id=datos["id"],
                        cliente=cliente,
                        habitacion=habitacion,
                        fechaInicio=datos["fechaInicio"],
                        fechaFin=datos["fechaFin"],
                        estado=datos["estado"]
                    )
                    self.reservas.append(reserva)
        except Exception as e:
            print(f"Error cargando reservas desde repositorio: {e}")
    
    def agregar_servicio_a_reserva(self, id_reserva, servicio_clase):
        reserva = self.buscar_reserva_por_id(id_reserva)
        if isinstance(reserva, Reserva) and reserva.estado == "Ocupada":
            reserva.agregar_servicio(servicio_clase)
            self.repositorio.guardar(reserva)
            return True
        return False


    def _obtener_clase_estado(self, nombre_estado):
        """Obtiene la clase de estado basada en el nombre"""
        estados = {
            'Disponible': Disponible,
            'Reservada': Reservada,
            'Ocupada': Ocupada,
            'PorLimpiar': PorLimpiar
        }
        return estados.get(nombre_estado, Disponible)

    def _guardar_habitaciones_en_repositorio(self):
        """Guarda todas las habitaciones en el repositorio"""
        for habitacion in self.habitaciones:
            self.repositorio.guardarHabitacion(habitacion)

    def getRepositorio(self) -> IRepositorioReservas:
        return self.repositorio

    def agregar_habitacion(self, habitacion):
        """Agrega una habitación y la guarda en el repositorio"""
        self.habitaciones.append(habitacion)
        self.repositorio.guardarHabitacion(habitacion)

    def buscar_habitacion_por_id(self, id_hab):
        return next((h for h in self.habitaciones if h.numero == id_hab), None)

    def obtener_habitaciones_disponibles(self):
        """Retorna lista de habitaciones disponibles"""
        return [h for h in self.habitaciones 
                if h.estado and h.estado.__class__.__name__ == 'Disponible']

    def agregar_reserva(self, reserva: Reserva):
        self.reservas.append(reserva)
        self.repositorio.guardar(reserva)

    def buscar_reserva_por_id(self, id_reserva):
        # Primero buscar en memoria
        reserva_memoria = next((r for r in self.reservas if r.id == id_reserva), None)
        if reserva_memoria:
            return reserva_memoria
        
        # Si no está en memoria, buscar en repositorio
        datos_reserva = self.repositorio.buscarPorId(id_reserva)
        return datos_reserva

    def cancelar_reserva(self, id_reserva):
        reserva = self.buscar_reserva_por_id(id_reserva)
        if reserva:
            # Obtener número de habitación
            numero_habitacion = None
            if hasattr(reserva, 'habitacion') and reserva.habitacion:
                numero_habitacion = reserva.habitacion.numero
            elif isinstance(reserva, dict):
                numero_habitacion = reserva.get('habitacion')
            
            # Cambiar estado de la habitación a disponible
            if numero_habitacion:
                habitacion = self.buscar_habitacion_por_id(numero_habitacion)
                if habitacion:
                    estado_disponible = Disponible()
                    habitacion.cambiarEstado(estado_disponible)
                    self.repositorio.guardarHabitacion(habitacion)
            
            # Remover de memoria si está ahí
            if reserva in self.reservas:
                self.reservas.remove(reserva)
            
            # Eliminar del repositorio
            self.repositorio.eliminar(id_reserva)
            return True
        return False

    def crear_reserva(self, cliente, habitacion, fecha_inicio, fecha_fin):
        # Generar ID único
        nuevo_id = self._generar_nuevo_id()
        
        nueva_reserva = Reserva(
            id=nuevo_id,
            cliente=cliente,
            habitacion=habitacion,
            fechaInicio=fecha_inicio,
            fechaFin=fecha_fin,
            estado="Reservada"
        )
        
        # Cambiar estado de la habitación a reservada
        estado_reservada = Reservada()
        habitacion.cambiarEstado(estado_reservada)
        self.repositorio.guardarHabitacion(habitacion)
        
        # Agregar reserva
        self.reservas.append(nueva_reserva)
        self.repositorio.guardar(nueva_reserva)
        
        return nueva_reserva

    def _generar_nuevo_id(self):
        """Genera un nuevo ID único para las reservas"""
        # Buscar el ID más alto tanto en memoria como en repositorio
        max_id_memoria = max([reserva.id for reserva in self.reservas], default=0)
        
        todas_reservas = self.repositorio.obtenerTodas()
        max_id_repositorio = max([r.get('id', 0) for r in todas_reservas], default=0)
        
        return max(max_id_memoria, max_id_repositorio) + 1

    def checkin(self, id_reserva):
        reserva = self.buscar_reserva_por_id(id_reserva)
        if reserva:
            estado_actual = reserva.get('estado') if isinstance(reserva, dict) else getattr(reserva, 'estado', None)
            
            if estado_actual == "Reservada":
                # Actualizar estado de la reserva
                if isinstance(reserva, dict):
                    reserva['estado'] = "Ocupada"
                else:
                    reserva.estado = "Ocupada"
                
                # Obtener número de habitación y cambiar su estado
                numero_habitacion = reserva.get('habitacion') if isinstance(reserva, dict) else reserva.habitacion.numero
                habitacion = self.buscar_habitacion_por_id(numero_habitacion)
                
                if habitacion:
                    estado_ocupada = Ocupada()
                    habitacion.cambiarEstado(estado_ocupada)
                    self.repositorio.guardarHabitacion(habitacion)
                
                # Actualizar en repositorio
                if not isinstance(reserva, dict):
                    self.repositorio.guardar(reserva)
                
                return True
        return False

    def checkout(self, id_reserva):
        reserva = self.buscar_reserva_por_id(id_reserva)
        if reserva:
            estado_actual = reserva.get('estado') if isinstance(reserva, dict) else getattr(reserva, 'estado', None)
            
            if estado_actual == "Ocupada":
                # Actualizar estado de la reserva
                if isinstance(reserva, dict):
                    reserva['estado'] = "Finalizada"
                else:
                    reserva.estado = "Finalizada"
                
                # Obtener número de habitación y cambiar su estado a por limpiar
                numero_habitacion = reserva.get('habitacion') if isinstance(reserva, dict) else reserva.habitacion.numero
                habitacion = self.buscar_habitacion_por_id(numero_habitacion)
                
                if habitacion:
                    estado_por_limpiar = PorLimpiar()
                    habitacion.cambiarEstado(estado_por_limpiar)
                    self.repositorio.guardarHabitacion(habitacion)
                
                # Generar factura (si trabajas con objetos Reserva completos)
                factura = None
                if not isinstance(reserva, dict):
                    if not hasattr(reserva, 'factura') or reserva.factura is None:
                        reserva.factura = Factura(reserva)
                        reserva.factura.generarFactura()
                    factura = reserva.factura
                    
                    # Actualizar en repositorio
                    self.repositorio.guardar(reserva)
                
                return factura
        return None

    def crear_habitacion(self, tipo, factory):
        # Obtener el siguiente número disponible
        if not self.habitaciones:
            nuevo_numero = 101  # Primer número si no hay habitaciones
        else:
            # Obtener el número más alto de las habitaciones existentes
            max_numero = max(h.numero for h in self.habitaciones)
            nuevo_numero = max_numero + 1  # Siguiente número disponible
            habitacion = factory.crearHabitacion(tipo, nuevo_numero)

        # Asignar estado inicial: Disponible
        estado = Disponible()
        habitacion.cambiarEstado(estado)

        self.habitaciones.append(habitacion)
        self.repositorio.guardarHabitacion(habitacion)

        return habitacion


    def limpiar_habitacion(self, numero_habitacion):
        """Cambia el estado de una habitación de PorLimpiar a Disponible"""
        habitacion = self.buscar_habitacion_por_id(numero_habitacion)
        if habitacion and habitacion.estado.__class__.__name__ == 'PorLimpiar':
            estado_disponible = Disponible()
            habitacion.cambiarEstado(estado_disponible)
            self.repositorio.guardarHabitacion(habitacion)
            return True
        return False

    def obtener_estadisticas(self):
        """Retorna estadísticas del hotel"""
        total_habitaciones = len(self.habitaciones)
        disponibles = len([h for h in self.habitaciones 
                          if h.estado.__class__.__name__ == 'Disponible'])
        reservadas = len([h for h in self.habitaciones 
                         if h.estado.__class__.__name__ == 'Reservada'])
        ocupadas = len([h for h in self.habitaciones 
                       if h.estado.__class__.__name__ == 'Ocupada'])
        por_limpiar = len([h for h in self.habitaciones 
                          if h.estado.__class__.__name__ == 'PorLimpiar'])
        
        total_reservas = len(self.repositorio.obtenerTodas())
        
        return {
            'total_habitaciones': total_habitaciones,
            'disponibles': disponibles,
            'reservadas': reservadas,
            'ocupadas': ocupadas,
            'por_limpiar': por_limpiar,
            'total_reservas': total_reservas
        }