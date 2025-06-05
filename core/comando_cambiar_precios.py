
from core.comando import Comando


class CambiarPreciosCommand(Comando):
    """
    Comando para cambiar precios de tipos de habitaciones.
    """

    def __init__(self, nuevos_precios: dict, repositorio):
        """
        Args:
            nuevos_precios (dict): Diccionario con tipos como clave y precios como valor
            repositorio: Repositorio para guardar los cambios
        """
        self.nuevos_precios = nuevos_precios
        self.repositorio = repositorio
        self.precios_anteriores = {}

    def ejecutar(self):
        """
        Ejecuta el cambio de precios.
        """
        # Guardar precios anteriores para posible deshacer
        for tipo in self.nuevos_precios.keys():
            precio_anterior = self.repositorio.obtener_precio_tipo(tipo)
            if precio_anterior is not None:
                self.precios_anteriores[tipo] = precio_anterior

        # Aplicar nuevos precios
        for tipo, precio in self.nuevos_precios.items():
            self.repositorio.guardar_precio_tipo(tipo, precio)

        return True

    def deshacer(self):
        """
        Deshace el cambio de precios.
        """
        for tipo, precio_anterior in self.precios_anteriores.items():
            self.repositorio.guardar_precio_tipo(tipo, precio_anterior)
