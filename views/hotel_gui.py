import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from core.comando_cambiar_precios import CambiarPreciosCommand
from core.reserva_manager import ReservaManager
from core.factory import HabitacionFactory
from core.cliente import Cliente
from core.servicios import ServicioRestaurante, ServicioLimpieza, ServicioAsistencia
from core.invocador import InvocadorComando
from core.crear_reserva_command import CrearReservaCommand
from core.registrar_checkin_command import RegistrarCheckInCommand
from core.registrar_checkout_command import RegistrarCheckOutCommand
from core.crear_habitacion_command import CrearHabitacionCommand
from core.cancelar_reserva_command import CancelarReservaCommand
from datetime import datetime, date
import calendar

# Paleta de colores y fuente
COLORES_UI = {
    "fondo": "#f2f2f2",
    "boton": "#4CAF50",
    "boton_secundario": "#3498db",
    "boton_texto": "white",
    "header": "#2c3e50",
    "texto_header": "white",
    "card": "#ffffff",
    "borde_card": "#cccccc"
}
FUENTE_GENERAL = ("Segoe UI", 11)
FUENTE_TITULO = ("Segoe UI", 16, "bold")
FUENTE_HEADER = ("Segoe UI", 18, "bold")

class MenuPrincipal(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=COLORES_UI["fondo"])
        self.controlador = controlador

        tk.Label(self, text="Sistema de Gestión Hotelera", font=FUENTE_HEADER,
                 bg=COLORES_UI["header"], fg=COLORES_UI["texto_header"], pady=20).pack(fill="x")
        tk.Button(self, text="Habitaciones", width=30, font=FUENTE_GENERAL, bg=COLORES_UI["boton"], fg=COLORES_UI["boton_texto"],
                  command=self.controlador.mostrar_vista_habitaciones).pack(pady=10)
        tk.Button(self, text="Reservas", width=30, font=FUENTE_GENERAL, bg=COLORES_UI["boton_secundario"], fg=COLORES_UI["boton_texto"],
                  command=self.controlador.mostrar_vista_reservas).pack(pady=10)
        tk.Button(self, text="Salir", width=30, font=FUENTE_GENERAL,
                  command=master.quit).pack(pady=10)

class Vistacrear_habitaciones(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg=COLORES_UI["fondo"])
        self.controlador = controlador
        self.manager = ReservaManager.getInstancia()
        self.factory = HabitacionFactory()
        self.invocador = InvocadorComando(self.manager)

        tk.Label(self, text="Crear nueva habitación", font=FUENTE_TITULO, bg=COLORES_UI["fondo"]).pack(pady=20)
        form_frame = tk.Frame(self, bg=COLORES_UI["fondo"])
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Tipo de habitación:", font=FUENTE_GENERAL, bg=COLORES_UI["fondo"]).pack(pady=5)
        self.tipo = tk.StringVar(value="estandar")
        for t in ["estandar", "doble", "suite"]:
            tk.Radiobutton(form_frame, text=t.capitalize(), variable=self.tipo, value=t, font=FUENTE_GENERAL,
                           bg=COLORES_UI["fondo"]).pack(anchor="w")

        tk.Button(form_frame, text="Crear habitación", font=FUENTE_GENERAL, bg=COLORES_UI["boton"], fg=COLORES_UI["boton_texto"],
                  command=self.crear_habitacion).pack(pady=15)
        tk.Button(self, text="Ir a vista de habitaciones", font=FUENTE_GENERAL,
                  command=self.controlador.mostrar_vista_habitaciones).pack(pady=10)
        tk.Button(self, text="← Volver al Menú Principal", 
         font=FUENTE_GENERAL, 
         bg="#95a5a6", fg="white", 
         width=30,
         command=self.controlador.mostrar_menu_principal).pack(pady=5)

    def crear_habitacion(self):
        try:
            comando = CrearHabitacionCommand(self.tipo.get(), self.factory, self.manager)
            self.invocador.establecer_comando(comando)
            habitacion_creada = self.invocador.ejecutar_comando()
            messagebox.showinfo("Éxito", f"Habitación ({habitacion_creada.get_descripcion()}) creada exitosamente.")
            self.controlador.mostrar_vista_habitaciones()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la habitación:\n{e}")
class DialogoCambiarPrecios:
    """Diálogo para cambiar precios de tipos de habitaciones."""

    def __init__(self, parent, repositorio, callback):
        self.repositorio = repositorio
        self.callback = callback
        
        # Crear ventana
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Cambiar Precios de Habitaciones")
        self.ventana.geometry("400x300")
        self.ventana.resizable(False, False)
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Centrar ventana
        self.ventana.geometry("+{}+{}".format(
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50
        ))
        
        self.crear_widgets()
        self.cargar_precios_actuales()

    def crear_widgets(self):
        """Crea los widgets del diálogo."""
        # Título
        tk.Label(self.ventana, text="Configurar Precios por Tipo de Habitación", 
                font=("Arial", 14, "bold")).pack(pady=10)

        # Frame principal
        main_frame = tk.Frame(self.ventana)
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Crear campos para cada tipo de habitación
        self.entries = {}
        tipos = [
            ("estandar", "Habitación Estándar"),
            ("doble", "Habitación Doble"),
            ("suite", "Suite")
        ]

        for i, (tipo, descripcion) in enumerate(tipos):
            # Label
            tk.Label(main_frame, text=f"{descripcion}:", font=("Arial", 11)).grid(
                row=i, column=0, sticky="w", pady=5, padx=(0, 10)
            )
            
            # Entry con validación numérica
            entry = tk.Entry(main_frame, font=("Arial", 11), width=15)
            entry.grid(row=i, column=1, pady=5, sticky="ew")
            
            # Label para mostrar precio actual
            label_actual = tk.Label(main_frame, text="", font=("Arial", 9), fg="gray")
            label_actual.grid(row=i, column=2, sticky="w", padx=(5, 0))
            
            self.entries[tipo] = {
                'entry': entry,
                'label_actual': label_actual
            }

        # Configurar grid weights
        main_frame.grid_columnconfigure(1, weight=1)

        # Frame para botones
        button_frame = tk.Frame(self.ventana)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Guardar", bg="lightgreen", 
                 command=self.guardar_precios, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancelar", bg="lightcoral", 
                 command=self.ventana.destroy, width=10).pack(side=tk.LEFT, padx=5)

    def cargar_precios_actuales(self):
        """Carga los precios actuales desde el repositorio."""
        precios_actuales = self.repositorio.obtener_todos_precios_tipos()
        
        # Precios por defecto si no existen en el repositorio
        precios_default = {
            "estandar": 100.0,
            "doble": 150.0,
            "suite": 250.0
        }

        for tipo, widgets in self.entries.items():
            precio_actual = precios_actuales.get(tipo, precios_default[tipo])
            
            # Llenar el campo de entrada con el precio actual
            widgets['entry'].delete(0, tk.END)
            widgets['entry'].insert(0, str(precio_actual))
            
            # Mostrar precio actual
            widgets['label_actual'].config(text=f"(Actual: ${precio_actual:.2f})")

    def guardar_precios(self):
        """Valida y guarda los nuevos precios."""
        try:
            nuevos_precios = {}
            
            for tipo, widgets in self.entries.items():
                precio_str = widgets['entry'].get().strip()
                
                if not precio_str:
                    messagebox.showerror("Error", f"Por favor ingrese un precio para {tipo}")
                    return
                
                try:
                    precio = float(precio_str)
                    if precio <= 0:
                        raise ValueError("El precio debe ser mayor a 0")
                    nuevos_precios[tipo] = precio
                except ValueError:
                    messagebox.showerror("Error", f"Precio inválido para {tipo}. Ingrese un número válido mayor a 0.")
                    return

            # Confirmar cambios
            mensaje = "¿Está seguro de cambiar los precios?\n\n"
            for tipo, precio in nuevos_precios.items():
                mensaje += f"{tipo.capitalize()}: ${precio:.2f}\n"
            
            if messagebox.askyesno("Confirmar", mensaje):
                # Ejecutar callback con los nuevos precios
                self.callback(nuevos_precios)
                self.ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar precios:\n{e}")

class VistaHabitaciones(tk.Frame):
    COLORES_ESTADO = {
        "Disponible": "lightgreen",
        "Reservada": "orange", 
        "Ocupada": "red",
        "PorLimpiar": "lightblue",
        "Deshabilitada": "grey"
    }

    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        self.manager = ReservaManager.getInstancia()
        self.factory = HabitacionFactory(self.manager.getRepositorio())
        self.invocador = InvocadorComando(self.manager)

        # Título y botones superiores
        header_frame = tk.Frame(self)
        header_frame.pack(pady=10, fill="x")
        
        tk.Label(header_frame, text="Gestión de Habitaciones", font=("Arial", 16)).pack()
        
        # Frame para botones de acción
        button_frame = tk.Frame(header_frame)
        button_frame.pack(pady=10)

        # Frame para filtros
        filter_frame = tk.Frame(header_frame)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filtrar por estado:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.filtro_estado = tk.StringVar(value="Todos")
        estados = ["Todos", "Disponible", "Reservada", "Ocupada", "PorLimpiar","Deshabilitada"]

        for estado in estados:
            tk.Radiobutton(filter_frame, text=estado, variable=self.filtro_estado, 
                        value=estado, command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Nueva Habitación", bg="lightblue", 
                 command=self.mostrar_dialog_crear_habitacion).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Actualizar Lista", 
                 command=self.actualizar_lista).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Limpiar Habitación", bg="lightyellow",
                 command=self.mostrar_dialog_limpiar).pack(side=tk.LEFT, padx=5)
        tk.Button(self, text="← Volver al Menú Principal", 
            font=("Segoe UI", 11), 
            bg="#95a5a6", fg="white", 
            pady=8, padx=20,
            command=self.controlador.mostrar_menu_principal).pack(pady=15)
        tk.Button(button_frame, text="Cambiar Precios", bg="lightgreen", 
                 command=self.mostrar_dialog_cambiar_precios).pack(side=tk.LEFT, padx=5)


        # Frame para la lista de habitaciones
        self.frame_lista = tk.Frame(self)
        self.frame_lista.pack(pady=10, fill="both", expand=True)

        # Botón volver
        tk.Button(self, text="Volver al Menú Principal", 
                 command=self.controlador.mostrar_menu_principal).pack(pady=10)
        
        self.actualizar_lista()

    def columnas_por_fila(self):
        ancho = self.winfo_width()
        if ancho <= 600:
            return 2
        elif ancho <= 900:
            return 3
        elif ancho <= 1200:
            return 4
        else:
            return 5

    def mostrar_dialog_crear_habitacion(self):
        dialog = crear_habitacionDialog(self, self.crear_habitacion_callback)

    def crear_habitacion_callback(self, tipo_habitacion):
        """Callback que se ejecuta cuando se confirma la creación de una habitación"""
        try:
            comando = CrearHabitacionCommand(tipo_habitacion, self.factory, self.manager)
            self.invocador.establecer_comando(comando)
            habitacion_creada = self.invocador.ejecutar_comando()
            
            messagebox.showinfo("Éxito", 
                f"Habitación {habitacion_creada.numero} ({habitacion_creada.get_descripcion()}) creada exitosamente.")
            self.actualizar_lista()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la habitación:\n{e}")

    def mostrar_dialog_limpiar(self):
        """Muestra un diálogo para seleccionar habitación a limpiar"""
        habitaciones_por_limpiar = [h for h in self.manager.habitaciones 
                                   if h.estado.__class__.__name__ == 'PorLimpiar']
        
        if not habitaciones_por_limpiar:
            messagebox.showinfo("Información", "No hay habitaciones que necesiten limpieza.")
            return
        
        # Crear lista de opciones
        opciones = [f"Habitación {h.numero} - {h.get_descripcion()}" for h in habitaciones_por_limpiar]
        
        dialog = SeleccionarHabitacionDialog(self, opciones, self.limpiar_habitacion_callback)

    def limpiar_habitacion_callback(self, seleccion):
        """Callback para limpiar habitación seleccionada"""
        try:
            # Extraer número de habitación de la selección
            numero_habitacion = int(seleccion.split()[1])
            
            if self.manager.limpiar_habitacion(numero_habitacion):
                messagebox.showinfo("Éxito", f"Habitación {numero_habitacion} ha sido limpiada y está disponible.")
                self.actualizar_lista()
            else:
                messagebox.showerror("Error", "No se pudo limpiar la habitación.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar habitación:\n{e}")
    
    def mostrar_dialog_cambiar_precios(self):
        """Muestra el diálogo para cambiar precios de habitaciones."""
        dialog = DialogoCambiarPrecios(self, self.manager.getRepositorio(), self.cambiar_precios_callback)

    def cambiar_precios_callback(self, nuevos_precios):
        """Callback que se ejecuta cuando se confirma el cambio de precios."""
        try:
            comando = CambiarPreciosCommand(nuevos_precios, self.manager.getRepositorio())
            self.invocador.establecer_comando(comando)
            resultado = self.invocador.ejecutar_comando()
            
            if resultado:
                messagebox.showinfo("Éxito", "Precios actualizados correctamente.")
                # Actualizar factory con repositorio actualizado
                self.factory = HabitacionFactory(self.manager.getRepositorio())
                # Opcional: actualizar habitaciones existentes
                self.actualizar_precios_habitaciones_existentes()
            else:
                messagebox.showerror("Error", "No se pudieron actualizar los precios.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar precios:\n{e}")

    def actualizar_precios_habitaciones_existentes(self):
        """Actualiza los precios de las habitaciones existentes."""
        repositorio = self.manager.getRepositorio()
        
        for habitacion in self.manager.habitaciones:
            tipo = habitacion.__class__.__name__.replace("Habitacion", "").lower()
            nuevo_precio = repositorio.obtener_precio_tipo(tipo)
            
            if nuevo_precio is not None:
                habitacion.precio = nuevo_precio
                # Guardar habitación actualizada en repositorio
                repositorio.guardar_habitacion(habitacion)

    def actualizar_lista(self):
        """Actualiza la lista visual de habitaciones"""
        # Limpiar widgets existentes
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        
        habitaciones_filtradas = self.filtrar_habitaciones()

        if not habitaciones_filtradas:
            texto = "No hay habitaciones creadas." if not self.manager.habitaciones else f"No hay habitaciones con estado '{self.filtro_estado.get()}'."
            tk.Label(self.frame_lista, text=texto, 
                    font=("Arial", 12)).pack(pady=20)
            return

        # Crear frame con scroll si hay muchas habitaciones
        contenedor_scroll = tk.Frame(self.frame_lista)
        contenedor_scroll.pack(fill="both", expand=True)

        canvas = tk.Canvas(contenedor_scroll, height=600)
        scrollbar = tk.Scrollbar(contenedor_scroll, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Permitir scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

        # Filtrar habitaciones según el estado seleccionado
        habitaciones_filtradas = self.filtrar_habitaciones()

        # Crear cards de habitaciones
        for habitacion in habitaciones_filtradas:
            self.crear_card_habitacion(scrollable_frame, habitacion)

    def filtrar_habitaciones(self):
        """Filtra las habitaciones según el estado seleccionado"""
        if self.filtro_estado.get() == "Todos":
            return self.manager.habitaciones
        
        estado_seleccionado = self.filtro_estado.get()
        return [h for h in self.manager.habitaciones 
                if h.estado.__class__.__name__ == estado_seleccionado]
    
    def deshabilitar_habitacion(self, seleccion):
        """Callback para limpiar habitación seleccionada"""
        try:
            # Extraer número de habitación de la selección
            numero_habitacion = int(seleccion.split()[1])

            if self.manager.deshabilitar_habitacion(numero_habitacion):
                messagebox.showinfo("Éxito", f"Habitación {numero_habitacion} ha sido deshabilitada.")
                self.actualizar_lista()
            else:
                messagebox.showerror("Error", "No se pudo deshabilitar la habitación.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al deshabilitar habitación:\n{e}")

    def habilitar_habitacion(self, seleccion):
        """Callback para limpiar habitación seleccionada"""
        try:
            # Extraer número de habitación de la selección
            numero_habitacion = int(seleccion.split()[1])

            if self.manager.habilitar_habitacion(numero_habitacion):
                messagebox.showinfo("Éxito", f"Habitación {numero_habitacion} ha sido habilitada.")
                self.actualizar_lista()
            else:
                messagebox.showerror("Error", "No se pudo habilitar la habitación.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al habilitar habitación:\n{e}")

    def crear_card_habitacion(self, parent, habitacion):
        """Crea una tarjeta visual para una habitación"""
        estado_clase = habitacion.estado.__class__.__name__
        color = self.COLORES_ESTADO.get(estado_clase, "white")
        
        frame = tk.Frame(parent, bd=2, relief=tk.RAISED, bg=color, padx=10, pady=5)
        frame.pack(pady=5, padx=10, fill="x")
        
        # Información de la habitación
        info_text = f"Habitación {habitacion.numero}\n{habitacion.get_descripcion()}\nEstado: {estado_clase}"
        tk.Label(frame, text=info_text, bg=color, font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Botón de acción según el estado
        if estado_clase == "PorLimpiar":
            tk.Button(frame, text="Limpiar", 
                     command=lambda: self.limpiar_habitacion_callback(f"Habitación {habitacion.numero}")).pack(side=tk.RIGHT)
        """elif estado_clase in ["Disponible", "Reservada", "Ocupada"]:
            tk.Button(frame, text="Cambiar Estado", 
                     command=lambda: self.cambiar_estado(habitacion)).pack(side=tk.RIGHT)"""
        if estado_clase != "Deshabilitada" and estado_clase != "Ocupada" and estado_clase != "Reservada":
            tk.Button(frame, text="Deshabilitar",
                  command=lambda: self.deshabilitar_habitacion(f"Habitación {habitacion.numero}")).pack(side=tk.RIGHT, padx=5)
        if estado_clase == "Deshabilitada":
            tk.Button(frame, text="Habilitar",
                  command=lambda: self.habilitar_habitacion(f"Habitación {habitacion.numero}")).pack(side=tk.RIGHT, padx=5)

    def cambiar_estado(self, habitacion):
        """Cambia el estado de una habitación según su ciclo"""
        habitacion.manejar_estado()
        self.actualizar_lista()

class crear_habitacionDialog:
    def __init__(self, parent, callback):
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Crear Nueva Habitación")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Centrar el diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        tk.Label(self.dialog, text="Seleccione el tipo de habitación:", 
                font=("Arial", 12)).pack(pady=20)
        
        self.tipo_var = tk.StringVar(value="estandar")
        
        tipos_frame = tk.Frame(self.dialog)
        tipos_frame.pack(pady=10)
        
        for tipo in ["estandar", "doble", "suite"]:
            tk.Radiobutton(tipos_frame, text=tipo.capitalize(), 
                          variable=self.tipo_var, value=tipo).pack(anchor="w")
        
        buttons_frame = tk.Frame(self.dialog)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Crear", bg="lightgreen",
                 command=self.crear).pack(side="left", padx=10)
        tk.Button(buttons_frame, text="Cancelar", 
                 command=self.dialog.destroy).pack(side="left", padx=10)
    
    def crear(self):
        self.callback(self.tipo_var.get())
        self.dialog.destroy()

class SeleccionarHabitacionDialog:
    def __init__(self, parent, opciones, callback):
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Seleccionar Habitación")
        self.dialog.geometry("350x250")
        self.dialog.resizable(False, False)
        
        # Centrar el diálogo
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        tk.Label(self.dialog, text="Seleccione la habitación:", 
                font=("Arial", 12)).pack(pady=10)
        
        self.seleccion_var = tk.StringVar(value=opciones[0] if opciones else "")
        
        opciones_frame = tk.Frame(self.dialog)
        opciones_frame.pack(pady=10, fill="both", expand=True)
        
        for opcion in opciones:
            tk.Radiobutton(opciones_frame, text=opcion, 
                          variable=self.seleccion_var, value=opcion).pack(anchor="w", padx=20)
        
        buttons_frame = tk.Frame(self.dialog)
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="Seleccionar", bg="lightgreen",
                 command=self.seleccionar).pack(side="left", padx=10)
        tk.Button(buttons_frame, text="Cancelar", 
                 command=self.dialog.destroy).pack(side="left", padx=10)
    
    def seleccionar(self):
        if self.seleccion_var.get():
            self.callback(self.seleccion_var.get())
        self.dialog.destroy()

class VistaReservas(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master, bg="#f8f9fa")
        self.controlador = controlador
        self.manager = ReservaManager.getInstancia()
        self.factory = HabitacionFactory()
        self.invocador = InvocadorComando(self.manager)
        self.reserva_filtrada = None

        # Crear el contenedor principal con scroll
        self.crear_interfaz()

    def crear_interfaz(self):
        # Canvas y Scrollbar para hacer scrollable toda la vista
        canvas = tk.Canvas(self, bg="#f8f9fa")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Título principal
        title_frame = tk.Frame(self.scrollable_frame, bg="#2c3e50", pady=15)
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(title_frame, text="📅 Crear Nueva Reserva", 
                font=("Segoe UI", 18, "bold"), 
                bg="#2c3e50", fg="white").pack()

        # Frame principal del formulario
        form_frame = tk.Frame(self.scrollable_frame, bg="white", relief="raised", bd=1)
        form_frame.pack(fill="x", padx=20, pady=10)

        # Sección de información del cliente
        self.crear_seccion_cliente(form_frame)
        
        # Separador
        ttk.Separator(form_frame, orient="horizontal").pack(fill="x", pady=15)
        
        # Sección de fechas
        self.crear_seccion_fechas(form_frame)
        
        # Separador
        ttk.Separator(form_frame, orient="horizontal").pack(fill="x", pady=15)
        
        # Sección de habitación
        self.crear_seccion_habitacion(form_frame)
        
        # Separador
        ttk.Separator(form_frame, orient="horizontal").pack(fill="x", pady=15)
        
        # Sección de servicios
        self.crear_seccion_servicios(form_frame)
        
        # Botones de acción
        self.crear_botones_accion(form_frame)

        # Sección de reservas existentes
        self.crear_seccion_reservas_existentes()

        # Configurar el canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Permitir scroll con mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def crear_seccion_cliente(self, parent):
        """Crea la sección de información del cliente con campos adicionales"""
        cliente_frame = tk.Frame(parent, bg="white")
        cliente_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(cliente_frame, text="👤 Información del Cliente", 
                font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        
        # Frame para campos del cliente
        campos_frame = tk.Frame(cliente_frame, bg="white")
        campos_frame.pack(fill="x", pady=10)
        
        # Primera fila: Nombre y Documento
        fila1_frame = tk.Frame(campos_frame, bg="white")
        fila1_frame.pack(fill="x", pady=5)
        
        # Nombre del cliente
        nombre_frame = tk.Frame(fila1_frame, bg="white")
        nombre_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(nombre_frame, text="Nombre completo: *", 
                font=("Segoe UI", 10), bg="white", fg="#2c3e50").pack(anchor="w")
        self.cliente_nombre = tk.Entry(nombre_frame, font=("Segoe UI", 10), 
                                    relief="solid", bd=1)
        self.cliente_nombre.pack(fill="x", pady=2)
        
        # Documento
        doc_frame = tk.Frame(fila1_frame, bg="white")
        doc_frame.pack(side="left", fill="x", expand=True)
        tk.Label(doc_frame, text="Número de documento: *", 
                font=("Segoe UI", 10), bg="white", fg="#2c3e50").pack(anchor="w")
        self.cliente_doc = tk.Entry(doc_frame, font=("Segoe UI", 10), 
                                relief="solid", bd=1)
        self.cliente_doc.pack(fill="x", pady=2)
        
        # Segunda fila: Teléfono y Correo
        fila2_frame = tk.Frame(campos_frame, bg="white")
        fila2_frame.pack(fill="x", pady=5)
        
        # Teléfono
        tel_frame = tk.Frame(fila2_frame, bg="white")
        tel_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(tel_frame, text="Teléfono:", 
                font=("Segoe UI", 10), bg="white", fg="#2c3e50").pack(anchor="w")
        self.cliente_telefono = tk.Entry(tel_frame, font=("Segoe UI", 10), 
                                        relief="solid", bd=1)
        self.cliente_telefono.pack(fill="x", pady=2)
        
        # Correo electrónico
        correo_frame = tk.Frame(fila2_frame, bg="white")
        correo_frame.pack(side="left", fill="x", expand=True)
        tk.Label(correo_frame, text="Correo electrónico:", 
                font=("Segoe UI", 10), bg="white", fg="#2c3e50").pack(anchor="w")
        self.cliente_correo = tk.Entry(correo_frame, font=("Segoe UI", 10), 
                                    relief="solid", bd=1)
        self.cliente_correo.pack(fill="x", pady=2)
        
        # Tercera fila: Método de pago
        fila3_frame = tk.Frame(campos_frame, bg="white")
        fila3_frame.pack(fill="x", pady=5)
        
        metodo_pago_frame = tk.Frame(fila3_frame, bg="white")
        metodo_pago_frame.pack(side="left", fill="x", expand=True)
        tk.Label(metodo_pago_frame, text="Método de pago: *", 
                font=("Segoe UI", 10), bg="white", fg="#2c3e50").pack(anchor="w")
        
        self.cliente_metodo_pago = ttk.Combobox(metodo_pago_frame, 
                                            font=("Segoe UI", 10), 
                                            state="readonly",
                                            values=["Efectivo", "Tarjeta de Crédito", 
                                                    "Tarjeta de Débito", "Transferencia Bancaria", 
                                                    "PSE", "Nequi", "Daviplata"])
        self.cliente_metodo_pago.pack(fill="x", pady=2)
        self.cliente_metodo_pago.set("Efectivo")  # Valor por defecto
        
        # Nota sobre campos obligatorios
        nota_frame = tk.Frame(campos_frame, bg="white")
        nota_frame.pack(fill="x", pady=(10, 0))
        tk.Label(nota_frame, text="* Campos obligatorios", 
        font=("Segoe UI", 9, "italic"), bg="white", fg="gray").pack(anchor="w")

    def crear_seccion_fechas(self, parent):
        fechas_frame = tk.Frame(parent, bg="white")
        fechas_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(fechas_frame, text="📅 Fechas de Reserva", 
                font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        
        fechas_container = tk.Frame(fechas_frame, bg="white")
        fechas_container.pack(fill="x", pady=10)
        
        # Fecha de inicio
        inicio_frame = tk.Frame(fechas_container, bg="white")
        inicio_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Label(inicio_frame, text="Fecha de entrada:", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        
        fecha_inicio_container = tk.Frame(inicio_frame, bg="white")
        fecha_inicio_container.pack(fill="x")
        
        # Día, mes, año para fecha inicio
        self.dia_inicio = ttk.Combobox(fecha_inicio_container, width=5, state="readonly")
        self.dia_inicio.pack(side="left", padx=(0, 5))
        
        self.mes_inicio = ttk.Combobox(fecha_inicio_container, width=12, state="readonly")
        self.mes_inicio.pack(side="left", padx=(0, 5))
        
        self.año_inicio = ttk.Combobox(fecha_inicio_container, width=8, state="readonly")
        self.año_inicio.pack(side="left")
        
        # Fecha de fin
        fin_frame = tk.Frame(fechas_container, bg="white")
        fin_frame.pack(side="left", fill="x", expand=True)
        
        tk.Label(fin_frame, text="Fecha de salida:", 
                font=("Segoe UI", 10), bg="white").pack(anchor="w")
        
        fecha_fin_container = tk.Frame(fin_frame, bg="white")
        fecha_fin_container.pack(fill="x")
        
        # Día, mes, año para fecha fin
        self.dia_fin = ttk.Combobox(fecha_fin_container, width=5, state="readonly")
        self.dia_fin.pack(side="left", padx=(0, 5))
        
        self.mes_fin = ttk.Combobox(fecha_fin_container, width=12, state="readonly")
        self.mes_fin.pack(side="left", padx=(0, 5))
        
        self.año_fin = ttk.Combobox(fecha_fin_container, width=8, state="readonly")
        self.año_fin.pack(side="left")
        
        # Configurar los comboboxes de fecha
        self.configurar_selectores_fecha()

    def configurar_selectores_fecha(self):
        # Configurar días (1-31)
        dias = [str(i) for i in range(1, 32)]
        self.dia_inicio['values'] = dias
        self.dia_fin['values'] = dias
        
        # Configurar meses
        meses = [calendar.month_name[i] for i in range(1, 13)]
        self.mes_inicio['values'] = meses
        self.mes_fin['values'] = meses
        
        # Configurar años (año actual + 2 años hacia adelante)
        año_actual = datetime.now().year
        años = [str(año_actual + i) for i in range(3)]
        self.año_inicio['values'] = años
        self.año_fin['values'] = años
        
        # Establecer valores por defecto (hoy y mañana)
        hoy = datetime.now()
        mañana = datetime.now().replace(day=hoy.day + 1) if hoy.day < 28 else hoy.replace(month=hoy.month + 1, day=1)
        
        self.dia_inicio.set(str(hoy.day))
        self.mes_inicio.set(calendar.month_name[hoy.month])
        self.año_inicio.set(str(hoy.year))
        
        self.dia_fin.set(str(mañana.day))
        self.mes_fin.set(calendar.month_name[mañana.month])
        self.año_fin.set(str(mañana.year))
        
        # Bind para actualizar días según el mes seleccionado
        self.mes_inicio.bind('<<ComboboxSelected>>', lambda e: self.actualizar_dias('inicio'))
        self.mes_fin.bind('<<ComboboxSelected>>', lambda e: self.actualizar_dias('fin'))
        self.año_inicio.bind('<<ComboboxSelected>>', lambda e: self.actualizar_dias('inicio'))
        self.año_fin.bind('<<ComboboxSelected>>', lambda e: self.actualizar_dias('fin'))

    def actualizar_dias(self, tipo):
        """Actualiza los días disponibles según el mes y año seleccionado"""
        try:
            if tipo == 'inicio':
                mes_combo = self.mes_inicio
                año_combo = self.año_inicio
                dia_combo = self.dia_inicio
            else:
                mes_combo = self.mes_fin
                año_combo = self.año_fin
                dia_combo = self.dia_fin
            
            if mes_combo.get() and año_combo.get():
                mes_num = list(calendar.month_name).index(mes_combo.get())
                año = int(año_combo.get())
                dias_en_mes = calendar.monthrange(año, mes_num)[1]
                
                dias = [str(i) for i in range(1, dias_en_mes + 1)]
                dia_combo['values'] = dias
                
                # Si el día actual es mayor que los días del mes, ajustar
                if dia_combo.get() and int(dia_combo.get()) > dias_en_mes:
                    dia_combo.set(str(dias_en_mes))
        except:
            pass

    def crear_seccion_habitacion(self, parent):
        hab_frame = tk.Frame(parent, bg="white")
        hab_frame.pack(fill="x", padx=20, pady=15)
        
        header_frame = tk.Frame(hab_frame, bg="white")
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="🏨 Selección de Habitación", 
                font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50").pack(side="left")
        
        tk.Button(header_frame, text="🔄 Actualizar", 
                 font=("Segoe UI", 9), bg="#3498db", fg="white",
                 command=self.actualizar_habitaciones_disponibles).pack(side="right")
        
        self.hab_container = tk.Frame(hab_frame, bg="white")
        self.hab_container.pack(fill="x", pady=10)
        
        self.var_hab = tk.StringVar()
        self.actualizar_habitaciones_disponibles()
    
    def mostrar_dialogo_servicio(self, reserva):
        dialogo = tk.Toplevel(self)
        dialogo.title(f"Agregar servicio a reserva #{reserva.id}")
        dialogo.geometry("300x250")
        dialogo.resizable(False, False)
        dialogo.transient(self)
        dialogo.grab_set()

        tk.Label(dialogo, text="Selecciona un servicio adicional:",
                font=("Segoe UI", 11, "bold")).pack(pady=15)

        def aplicar(servicio_clase, nombre):
            exito = self.manager.agregar_servicio_a_reserva(reserva.id, servicio_clase)
            if exito:
                messagebox.showinfo("Servicio agregado", f"{nombre} agregado exitosamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el servicio.")
            dialogo.destroy()

        servicios = [
            ("🍽 Restaurante", ServicioRestaurante),
            ("🧹 Limpieza", ServicioLimpieza),
            ("🔧 Asistencia", ServicioAsistencia),
        ]

        for nombre, clase_servicio in servicios:
            tk.Button(dialogo, text=nombre,
                    width=25, font=("Segoe UI", 10),
                    command=lambda c=clase_servicio, n=nombre: aplicar(c, n)).pack(pady=5)

        tk.Button(dialogo, text="Cancelar", command=dialogo.destroy).pack(pady=10)


    def crear_seccion_servicios(self, parent):
        servicios_frame = tk.Frame(parent, bg="white")
        servicios_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(servicios_frame, text="🛎️ Servicios Adicionales", 
                font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        
        self.servicios = {
            "restaurante": tk.IntVar(),
            "limpieza": tk.IntVar(),
            "asistencia": tk.IntVar()
        }
        
        servicios_container = tk.Frame(servicios_frame, bg="white")
        servicios_container.pack(fill="x", pady=10)
        
        iconos = {"restaurante": "🍽️", "limpieza": "🧹", "asistencia": "🔧"}
        descripciones = {
            "restaurante": "Servicio de restaurante incluido",
            "limpieza": "Servicio de limpieza adicional",
            "asistencia": "Servicio de asistencia técnica"
        }
        
        for nombre, var in self.servicios.items():
            frame_servicio = tk.Frame(servicios_container, bg="white")
            frame_servicio.pack(fill="x", pady=2)
            
            tk.Checkbutton(frame_servicio, 
                          text=f"{iconos[nombre]} {nombre.capitalize()}", 
                          variable=var, 
                          font=("Segoe UI", 10),
                          bg="white").pack(side="left")
            
            tk.Label(frame_servicio, text=f"- {descripciones[nombre]}", 
                    font=("Segoe UI", 9), fg="gray", bg="white").pack(side="left", padx=(10, 0))

    def crear_botones_accion(self, parent):
        botones_frame = tk.Frame(parent, bg="white")
        botones_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Button(botones_frame, text="✅ Crear Reserva", 
                 font=("Segoe UI", 12, "bold"), 
                 bg="#27ae60", fg="white", 
                 pady=10, command=self.crear_reserva).pack(side="left", padx=(0, 10))
        
        tk.Button(botones_frame, text="↩️ Volver al Menú", 
                 font=("Segoe UI", 10), 
                 bg="#95a5a6", fg="white", 
                 pady=10, command=self.controlador.mostrar_menu_principal).pack(side="right")
    def busqueda_en_tiempo_real(self, event):
        """Busca reservas mientras el usuario escribe (opcional)"""
        texto = self.entrada_busqueda.get().strip()
        if not texto:
            self.mostrar_todas_reservas()
            return
        
        try:
            id_reserva = int(texto)
            reserva_encontrada = None
            for reserva in self.manager.reservas:
                if reserva.id == id_reserva:
                    reserva_encontrada = reserva
                    break
            
            self.reserva_filtrada = reserva_encontrada
            self.actualizar_lista_reservas()
        except ValueError:
            # Si no es un número válido, mostrar todas
            pass

    def crear_seccion_reservas_existentes(self):
        reservas_section = tk.Frame(self.scrollable_frame, bg="white", relief="raised", bd=1)
        reservas_section.pack(fill="x", padx=20, pady=20)
        # Frame para búsqueda
        busqueda_frame = tk.Frame(reservas_section, bg="white")
        busqueda_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(busqueda_frame, text="🔍 Buscar reserva por número:", 
                font=("Segoe UI", 11), bg="white").pack(side="left", padx=(0, 10))

        self.entrada_busqueda = tk.Entry(busqueda_frame, font=("Segoe UI", 10), width=15)
        self.entrada_busqueda.pack(side="left", padx=(0, 5))
        self.entrada_busqueda.bind('<KeyRelease>', self.busqueda_en_tiempo_real)


        tk.Button(busqueda_frame, text="Buscar", 
                font=("Segoe UI", 9), bg="#3498db", fg="white",
                command=self.buscar_reserva).pack(side="left", padx=(0, 5))

        tk.Button(busqueda_frame, text="Mostrar todas", 
                font=("Segoe UI", 9), bg="#95a5a6", fg="white",
                command=self.mostrar_todas_reservas).pack(side="left")
                
        header_reservas = tk.Frame(reservas_section, bg="#34495e", pady=10)
        header_reservas.pack(fill="x")
        
        tk.Label(header_reservas, text="📋 Gestionar Reservas Existentes", 
                font=("Segoe UI", 14, "bold"), 
                bg="#34495e", fg="white").pack()
        
        self.frame_reservas = tk.Frame(reservas_section, bg="white")
        self.frame_reservas.pack(fill="x", padx=15, pady=15)
        
        self.actualizar_lista_reservas()

    def obtener_fecha_desde_selectores(self, tipo):
        """Convierte los valores de los selectores a un objeto date"""
        try:
            if tipo == 'inicio':
                dia = int(self.dia_inicio.get())
                mes = list(calendar.month_name).index(self.mes_inicio.get())
                año = int(self.año_inicio.get())
            else:
                dia = int(self.dia_fin.get())
                mes = list(calendar.month_name).index(self.mes_fin.get())
                año = int(self.año_fin.get())
            
            return date(año, mes, dia)
        except (ValueError, AttributeError):
            raise ValueError(f"Valores de fecha {'de inicio' if tipo == 'inicio' else 'de fin'} inválidos")

    def actualizar_habitaciones_disponibles(self):
        """Actualiza la lista de habitaciones disponibles"""
        # Limpiar contenedor anterior
        for widget in self.hab_container.winfo_children():
            widget.destroy()
        
        disponibles = [h for h in self.manager.habitaciones if h.estado.__class__.__name__ == "Disponible"]
        
        if disponibles:
            tk.Label(self.hab_container, text="Habitaciones disponibles:", 
                    font=("Segoe UI", 10), bg="white").pack(anchor="w", pady=(0, 5))
            
            # Crear frame para las habitaciones con scroll horizontal si es necesario
            hab_scroll_frame = tk.Frame(self.hab_container, bg="white")
            hab_scroll_frame.pack(fill="x")
            
            self.var_hab.set(str(disponibles[0].numero))
            
            for i, habitacion in enumerate(disponibles):
                hab_button = tk.Radiobutton(hab_scroll_frame, 
                                          text=f"Hab. {habitacion.numero}\n({habitacion.get_descripcion()})",
                                          variable=self.var_hab, 
                                          value=str(habitacion.numero),
                                          font=("Segoe UI", 9),
                                          bg="white",
                                          indicatoron=False,
                                          selectcolor="#3498db",
                                          width=15, height=3)
                hab_button.pack(side="left", padx=5, pady=5)
        else:
            tk.Label(self.hab_container, 
                    text="⚠️ No hay habitaciones disponibles para reservar.", 
                    font=("Segoe UI", 11), fg="red", bg="white").pack(pady=10)

    def crear_reserva(self):
        try:
            # Validar campos obligatorios del cliente
            nombre = self.cliente_nombre.get().strip()
            doc = self.cliente_doc.get().strip()
            metodo_pago = self.cliente_metodo_pago.get()
            
            if not nombre or not doc or not metodo_pago:
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios del cliente.")
                return
            
            # Obtener campos opcionales
            telefono = self.cliente_telefono.get().strip()
            correo = self.cliente_correo.get().strip()
            
            # Crear objeto cliente con información completa
            cliente = Cliente(nombre, doc, telefono, correo, metodo_pago)
            
            # Validar datos del cliente
            es_valido, mensaje_error = cliente.validar_datos_completos()
            if not es_valido:
                messagebox.showerror("Error de validación", mensaje_error)
                return

            # Obtener fechas desde los selectores
            try:
                fecha_inicio = self.obtener_fecha_desde_selectores('inicio')
                fecha_fin = self.obtener_fecha_desde_selectores('fin')
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
            
            # Validar fechas
            if fecha_inicio >= fecha_fin:
                messagebox.showerror("Error", "La fecha de salida debe ser posterior a la fecha de entrada.")
                return
            
            if fecha_inicio < date.today():
                messagebox.showerror("Error", "La fecha de entrada no puede ser anterior a hoy.")
                return

            # Validar habitación seleccionada
            if not self.var_hab.get():
                messagebox.showerror("Error", "Por favor seleccione una habitación.")
                return

            num_hab = int(self.var_hab.get())
            habitacion = self.manager.buscar_habitacion_por_id(num_hab)

            # Aplicar servicios adicionales
            if self.servicios["restaurante"].get():
                habitacion = ServicioRestaurante(habitacion)
            if self.servicios["limpieza"].get():
                habitacion = ServicioLimpieza(habitacion)
            if self.servicios["asistencia"].get():
                habitacion = ServicioAsistencia(habitacion)

            # Crear la reserva
            comando = CrearReservaCommand(cliente, habitacion, fecha_inicio, fecha_fin, self.manager)
            self.invocador.establecer_comando(comando)
            self.invocador.ejecutar_comando()

            # Mensaje de confirmación más detallado
            mensaje_confirmacion = (
                f"✅ Reserva creada exitosamente:\n\n"
                f"Cliente: {nombre}\n"
                f"Documento: {doc}\n"
            )
            
            if telefono:
                mensaje_confirmacion += f"Teléfono: {telefono}\n"
            if correo:
                mensaje_confirmacion += f"Correo: {correo}\n"
                
            mensaje_confirmacion += (
                f"Método de pago: {metodo_pago}\n"
                f"Habitación: {num_hab}\n"
                f"Entrada: {fecha_inicio.strftime('%d/%m/%Y')}\n"
                f"Salida: {fecha_fin.strftime('%d/%m/%Y')}"
            )

            messagebox.showinfo("Reserva Creada", mensaje_confirmacion)
            
            # Limpiar formulario
            self.limpiar_formulario_completo()
            
            # Actualizar listas
            self.actualizar_lista_reservas()
            self.actualizar_habitaciones_disponibles()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la reserva:\n{e}")

    def limpiar_formulario_completo(self):
        """Limpia todos los campos del formulario después de crear una reserva"""
        # Campos del cliente
        self.cliente_nombre.delete(0, tk.END)
        self.cliente_doc.delete(0, tk.END)
        self.cliente_telefono.delete(0, tk.END)
        self.cliente_correo.delete(0, tk.END)
        self.cliente_metodo_pago.set("Efectivo")
        # Resetear servicios
        for var in self.servicios.values():
            var.set(0)

    def actualizar_lista_reservas(self):
        """Actualiza la lista visual de reservas existentes"""
        for widget in self.frame_reservas.winfo_children():
            widget.destroy()

        # Determinar qué reservas mostrar
        reservas_a_mostrar = []
        if self.reserva_filtrada:
            reservas_a_mostrar = [self.reserva_filtrada]
        else:
            reservas_a_mostrar = self.manager.reservas

        if not reservas_a_mostrar:
            texto = "No hay reservas registradas." if not self.manager.reservas else "No se encontró la reserva buscada."
            tk.Label(self.frame_reservas, text=texto, 
                    font=("Segoe UI", 11), bg="white", fg="gray").pack(pady=20)
            return

        for reserva in reservas_a_mostrar:
            # Frame para cada reserva
            reserva_frame = tk.Frame(self.frame_reservas, bg="#ecf0f1", relief="solid", bd=1)
            reserva_frame.pack(fill="x", pady=5, padx=5)
            
            # Información de la reserva
            info_frame = tk.Frame(reserva_frame, bg="#ecf0f1")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=8)
            
            # Primera línea: ID y cliente
            tk.Label(info_frame, 
                    text=f"Reserva #{reserva.id} - {reserva.cliente.nombre}", 
                    font=("Segoe UI", 11, "bold"), 
                    bg="#ecf0f1").pack(anchor="w")
            
            # Segunda línea: habitación y estado
            estado_color = {"Reservada": "#f39c12", "Ocupada": "#e74c3c", "Completada": "#27ae60"}
            tk.Label(info_frame, 
                    text=f"Habitación {reserva.habitacion.numero} | Estado: {reserva.estado}", 
                    font=("Segoe UI", 9), 
                    bg="#ecf0f1",
                    fg=estado_color.get(reserva.estado, "#34495e")).pack(anchor="w")

            # Botones de acción
            botones_frame = tk.Frame(reserva_frame, bg="#ecf0f1")
            botones_frame.pack(side="right", padx=10, pady=5)

            # Botón cancelar reserva
            if reserva.estado == "Reservada":
                tk.Button(botones_frame, text="Cancelar", 
                        font=("Segoe UI", 9), bg="#e67e22", fg="white",
                        command=lambda r=reserva: self.cancelar_reserva(r)).pack(pady=2)

            if reserva.estado == "Reservada":
                tk.Button(botones_frame, text="Check-in", 
                        font=("Segoe UI", 9), bg="#27ae60", fg="white",
                        command=lambda r=reserva: self.checkin(r)).pack(pady=2)
            elif reserva.estado == "Ocupada":
                tk.Button(botones_frame, text="Check-out", 
                        font=("Segoe UI", 9), bg="#e74c3c", fg="white",
                        command=lambda r=reserva: self.checkout(r)).pack(pady=2)
                
                tk.Button(botones_frame, text="Agregar servicio",
                        font=("Segoe UI", 9), bg="#3498db", fg="white",
                        command=lambda r=reserva: self.mostrar_dialogo_servicio(r)).pack(pady=2)
        
    def buscar_reserva(self):
        """Busca una reserva específica por número"""
        try:
            numero_reserva = self.entrada_busqueda.get().strip()
            if not numero_reserva:
                messagebox.showwarning("Advertencia", "Por favor ingrese un número de reserva.")
                return
            
            # Convertir a entero
            try:
                id_reserva = int(numero_reserva)
            except ValueError:
                messagebox.showerror("Error", "El número de reserva debe ser un número válido.")
                return
            
            # Buscar la reserva
            reserva_encontrada = None
            for reserva in self.manager.reservas:
                if reserva.id == id_reserva:
                    reserva_encontrada = reserva
                    break
            
            if reserva_encontrada:
                self.reserva_filtrada = reserva_encontrada
                messagebox.showinfo("Reserva encontrada", 
                                f"Reserva #{reserva_encontrada.id} encontrada:\n"
                                f"Cliente: {reserva_encontrada.cliente.nombre}\n"
                                f"Estado: {reserva_encontrada.estado}")
                self.actualizar_lista_reservas()
            else:
                self.reserva_filtrada = None
                messagebox.showwarning("No encontrada", f"No se encontró la reserva #{id_reserva}")
                self.actualizar_lista_reservas()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en la búsqueda: {e}")

    def mostrar_todas_reservas(self):
        """Muestra todas las reservas y limpia el filtro"""
        self.reserva_filtrada = None
        self.entrada_busqueda.delete(0, tk.END)
        self.actualizar_lista_reservas()


    def checkin(self, reserva):
        """Procesa el check-in de una reserva"""
        try:
            comando = RegistrarCheckInCommand(reserva.id, self.manager)
            self.invocador.establecer_comando(comando)
            self.invocador.ejecutar_comando()
            messagebox.showinfo("Check-in", f"Check-in realizado para la reserva #{reserva.id}")
            self.actualizar_lista_reservas()
        except Exception as e:
            messagebox.showerror("Error", f"Error en check-in: {e}")

    def checkout(self, reserva):
        """Procesa el check-out de una reserva"""
        try:
            comando = RegistrarCheckOutCommand(reserva.id, self.manager)
            self.invocador.establecer_comando(comando)
            self.invocador.ejecutar_comando()
            messagebox.showinfo("Check-out", f"Check-out realizado para la reserva #{reserva.id}")
            self.actualizar_lista_reservas()
            self.actualizar_habitaciones_disponibles()
        except Exception as e:
            messagebox.showerror("Error", f"Error en check-out: {e}")
    
    def cancelar_reserva(self, reserva):
        """Cancela una reserva y libera la habitación"""
        try:
            # Validar que la reserva se puede cancelar
            if reserva.estado == "Ocupada":
                messagebox.showerror(
                    "No se puede cancelar", 
                    f"No se puede cancelar la reserva #{reserva.id} porque el huésped ya hizo check-in.\n"
                    f"La habitación está ocupada."
                )
                return
            
            if reserva.estado == "Finalizada":
                messagebox.showerror(
                    "No se puede cancelar", 
                    f"No se puede cancelar la reserva #{reserva.id} porque ya está finalizada."
                )
                return
            
            # Confirmar la cancelación
            respuesta = messagebox.askyesno(
                "Confirmar cancelación", 
                f"¿Está seguro de cancelar la reserva #{reserva.id}?\n"
                f"Cliente: {reserva.cliente.nombre}\n"
                f"Estado: {reserva.estado}\n"
                f"Esta acción no se puede deshacer."
            )
            
            if respuesta:
                # Usar el comando para cancelar
                comando = CancelarReservaCommand(reserva.id, self.manager)
                self.invocador.establecer_comando(comando)
                resultado = self.invocador.ejecutar_comando()
                
                if resultado:
                    messagebox.showinfo("Cancelación exitosa", 
                                    f"La reserva #{reserva.id} ha sido cancelada.\n"
                                    f"La habitación {reserva.habitacion.numero} está ahora disponible.")
                    # Actualizar las listas
                    self.actualizar_lista_reservas()
                    self.actualizar_habitaciones_disponibles()
                else:
                    messagebox.showerror("Error", "No se pudo cancelar la reserva.")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cancelar la reserva: {e}")

class ControladorVentanas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Hotelero")
        self.frame_actual = None
        self.mostrar_menu_principal()

    def cambiar_vista(self, clase_vista):
        if self.frame_actual:
            self.frame_actual.pack_forget()
            self.frame_actual.destroy()
        self.frame_actual = clase_vista(self.root, self)
        self.frame_actual.pack(fill="both", expand=True)

    def mostrar_menu_principal(self):
        self.cambiar_vista(MenuPrincipal)

    def mostrar_vista_habitaciones(self):
        if not ReservaManager.getInstancia().habitaciones:
            self.cambiar_vista(Vistacrear_habitaciones)
        else:
            self.cambiar_vista(VistaHabitaciones)

    def mostrar_vista_reservas(self):
        self.cambiar_vista(VistaReservas)
