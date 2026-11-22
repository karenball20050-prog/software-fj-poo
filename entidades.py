"""Clase abstracta base y clase Cliente."""

import re                      # Expresiones regulares para validar el correo
from abc import ABC, abstractmethod  # Herramientas para clases abstractas

from excepciones import ClienteInvalidoError, ParametroFaltanteError
from logger import log


class EntidadBase(ABC):
    """Clase abstracta que representa una entidad general del sistema."""

    def __init__(self, identificador):
        # Atributo protegido con el identificador de la entidad
        self._id = identificador

    @property
    def id(self):
        """Devuelve el identificador (solo lectura: encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe describirse a sí misma (método abstracto)."""


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validaciones estrictas."""

    def __init__(self, identificador, nombre=None, correo=None, telefono=None):
        # Si falta algún dato obligatorio, lanzamos excepción específica
        if nombre is None or correo is None or telefono is None:
            raise ParametroFaltanteError("Faltan datos obligatorios del cliente")
        # Inicializamos la clase padre con el identificador
        super().__init__(identificador)
        # Asignamos usando las propiedades, para que se ejecuten las validaciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self):
        """Devuelve el nombre (atributo privado)."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # El nombre debe ser texto no vacío de al menos 3 caracteres
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r}")
        self.__nombre = valor.strip()

    # ---------- correo ----------
    @property
    def correo(self):
        """Devuelve el correo (atributo privado)."""
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Patrón sencillo: algo@dominio.ext
        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
        if not isinstance(valor, str) or not re.match(patron, valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = valor

    # ---------- teléfono ----------
    @property
    def telefono(self):
        """Devuelve el teléfono (atributo privado)."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        try:
            # Intentamos convertir a número para comprobar que solo hay dígitos
            int(valor)
        except (ValueError, TypeError) as e:
            # Encadenamiento de excepciones: conservamos la causa original con "from e"
            raise ClienteInvalidoError(f"Teléfono no numérico: {valor!r}") from e
        else:
            # Si la conversión funcionó, validamos la longitud (7 a 10 dígitos)
            texto = str(valor)
            if not (7 <= len(texto) <= 10) or not texto.isdigit():
                raise ClienteInvalidoError(f"Teléfono con longitud inválida: {valor!r}")
            self.__telefono = texto

    def describir(self):
        """Descripción textual del cliente (sobrescribe el método abstracto)."""
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | Tel: {self.telefono}"

    @classmethod
    def crear(cls, identificador, nombre=None, correo=None, telefono=None):
        """Fábrica segura: crea el cliente y registra éxito o error en el log."""
        try:
            cliente = cls(identificador, nombre, correo, telefono)
        except Exception as e:
            # Registramos el error y lo relanzamos para que lo gestione quien llamó
            log.error(f"Fallo al crear cliente {identificador}: {e}")
            raise
        else:
            # Solo se ejecuta si no hubo excepción
            log.info(f"Cliente creado: {cliente.describir()}")
            return cliente
