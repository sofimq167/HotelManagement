"""
Módulo que define la clase Cliente.
"""

class Cliente:
    """
    Representa a un cliente con información completa para reservas y facturación.

    Atributos:
        nombre (str): Nombre completo del cliente.
        documento (str): Documento de identidad del cliente.
        telefono (str): Número de teléfono del cliente.
        correo (str): Dirección de correo electrónico del cliente.
        metodo_pago (str): Método de pago preferido del cliente.
    """

    def __init__(self, nombre: str, documento: str, telefono: str = "", 
                 correo: str = "", metodo_pago: str = "Efectivo"):
        """
        Inicializa un nuevo cliente con información completa.

        Args:
            nombre (str): Nombre completo del cliente.
            documento (str): Documento de identidad del cliente.
            telefono (str, optional): Número de teléfono del cliente. Defaults to "".
            correo (str, optional): Correo electrónico del cliente. Defaults to "".
            metodo_pago (str, optional): Método de pago preferido. Defaults to "Efectivo".
        """
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono
        self.correo = correo
        self.metodo_pago = metodo_pago

    def __str__(self) -> str:
        """
        Retorna una representación legible del cliente.

        Returns:
            str: Representación del cliente en formato 'Nombre (ID: documento)'.
        """
        return f"{self.nombre} (ID: {self.documento})"

    def get_info_completa(self) -> str:
        """
        Retorna la información completa del cliente para facturas.

        Returns:
            str: Información completa del cliente formateada.
        """
        info = f"Nombre: {self.nombre}\n"
        info += f"Documento: {self.documento}\n"
        
        if self.telefono:
            info += f"Teléfono: {self.telefono}\n"
        
        if self.correo:
            info += f"Correo: {self.correo}\n"
        
        info += f"Método de pago: {self.metodo_pago}"
        
        return info

    def validar_datos_completos(self) -> tuple[bool, str]:
        """
        Valida que los datos del cliente estén completos para facturación.

        Returns:
            tuple[bool, str]: (True/False, mensaje de error si hay)
        """
        if not self.nombre.strip():
            return False, "El nombre es obligatorio"
        
        if not self.documento.strip():
            return False, "El documento es obligatorio"
        
        if self.correo and not self._validar_email(self.correo):
            return False, "El formato del correo electrónico no es válido"
        
        return True, ""

    def _validar_email(self, email: str) -> bool:
        """
        Valida el formato básico de un email.

        Args:
            email (str): Email a validar

        Returns:
            bool: True si el formato es válido, False en caso contrario
        """
        import re
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
