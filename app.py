import tkinter as tk
from views.hotel_gui import ControladorVentanas
from core.repositorio_bd import RepositorioBD
from core.reserva_manager import ReservaManager

def main():
    repositorio = RepositorioBD()
    manager = ReservaManager.getInstancia(repositorio)

    # Imprimir lista de habitaciones - Para verificar
    print("\nLista de habitaciones registradas")
    for hab in manager.habitaciones:
        estado = hab.estado.__class__.__name__ if hab.estado else "Sin estado"
        print(f"Habitación {hab.numero} - {hab.getDescripcion()} - ${hab.getPrecio()} - Estado: {estado}")
    
    # Imprimir lista de reservas - Para verificar
    print("\nLista de reservas registradas")
    for reserva in manager.reservas:
        print(f"Reserva ID: {reserva.id}, Cliente: {reserva.cliente.nombre}, "
        f"Habitación: {reserva.habitacion.numero}, "
        f"Check-in: {reserva.fechaInicio}, Check-out: {reserva.fechaFin}")


    root = tk.Tk()
    
    # Configurar la ventana para que se vea bien en diferentes sistemas
    root.tk.call('tk', 'scaling', 1.0)
    
    # Crear el controlador principal
    app = ControladorVentanas(root)
    
    # Iniciar el bucle principal
    root.mainloop()


if __name__ == "__main__":
    main()
