"""Módulo que define la clase base abstracta para comandos."""

from abc import ABC, abstractmethod


class Comando(ABC):
    """
    Clase abstracta base para comandos del sistema.

    Cada subclase debe implementar el método `ejecutar`.
    """

    @abstractmethod
    def ejecutar(self):
        """
        Ejecuta el comando. Este método debe ser implementado por las subclases.

        Raises:
            NotImplementedError: Si la subclase no implementa este método.
        """
        raise NotImplementedError("El método ejecutar debe ser implementado por la subclase.")
