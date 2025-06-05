import argparse
import tkinter as tk
from core.repositorio_archivo import RepositorioArchivo
from views.hotel_gui import ControladorVentanas
from core.repositorio_bd import RepositorioBD
from core.reserva_manager import ReservaManager

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--repositorio", choices=["bd", "archivo"], default="bd")
    args = parser.parse_args()

    sincronizar_repositorios()

    if args.repositorio == "bd":
        repositorio = RepositorioBD()
    else:
        repositorio = RepositorioArchivo()

    manager = ReservaManager.getInstancia(repositorio)

    root = tk.Tk()
    # Configurar la ventana para que se vea bien en diferentes sistemas
    root.tk.call('tk', 'scaling', 1.0)
    
    # Crear el controlador principal
    app = ControladorVentanas(root)
    
    # Iniciar el bucle principal
    root.mainloop()

def sincronizar_repositorios(ruta_bd="hotel.db"):
    repo_bd = RepositorioBD(ruta_bd)
    repo_json = RepositorioArchivo()

    # Obtener cantidades
    total_bd = len(repo_bd.obtener_todas()) + len(repo_bd.obtener_habitaciones()) + len(repo_bd.obtener_todos_precios_tipos())
    total_json = len(repo_json.obtener_todas()) + len(repo_json.obtener_habitaciones()) + len(repo_json.obtener_todos_precios_tipos())

    if total_bd >= total_json:
        print("Migrando desde base de datos a archivos JSON...")
        resultado = repo_json.migrar_desde_bd(repo_bd)
    else:
        print("Migrando desde archivos JSON a base de datos...")
        resultado = repo_json.migrar_hacia_bd(repo_bd)

    repo_bd.cerrar()
    return resultado

if __name__ == "__main__":
    main()
