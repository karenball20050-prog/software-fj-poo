"""Clase Reserva: integra cliente, servicio, duración y estado."""

from entidades import EntidadBase, Cliente
from servicios import Servicio
from excepciones import (ErrorSoftwareFJ, ReservaInvalidaError,
                         ServicioNoDisponibleError, OperacionNoPermitidaError,
                         CalculoInconsistenteError)
from logger import log


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    # Estados posibles de la reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    def __init__(self, identificador, cliente=None, servicio=None, horas=None):
        super().__init__(identificador)
        # Validamos los tipos de los objetos recibidos
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido")
        # La duración debe ser un número positivo
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ReservaInvalidaError(f"Duración inválida: {horas!r}")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.PENDIENTE  # Toda reserva inicia pendiente

    @property
    def estado(self):
        """Estado actual de la reserva (solo lectura)."""
        return self._estado

    def confirmar(self):
        """Confirma la reserva si está pendiente y el servicio está disponible."""
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' no está disponible")
        self._estado = self.CONFIRMADA
        log.info(f"Reserva {self.id} confirmada")

    def cancelar(self):
        """Cancela la reserva si no estaba cancelada."""
        if self._estado == self.CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada")
        self._estado = self.CANCELADA
        log.info(f"Reserva {self.id} cancelada")

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Confirma la reserva y calcula su costo con manejo completo de excepciones."""
        try:
            self.confirmar()
            costo = self._servicio.calcular_costo(self._horas, impuesto, descuento)
        except ErrorSoftwareFJ as e:
            # Error propio del sistema: lo registramos y lo relanzamos
            log.error(f"Reserva {self.id} no procesada: {e}")
            raise
        except Exception as e:
            # Error inesperado: lo encadenamos dentro de una excepción propia
            log.error(f"Error inesperado en reserva {self.id}: {e}")
            raise CalculoInconsistenteError("Fallo inesperado al procesar") from e
        else:
            # Solo se ejecuta si no hubo errores
            log.info(f"Reserva {self.id} procesada. Costo total: ${costo}")
            return costo
        finally:
            # Siempre se ejecuta, haya o no error
            log.info(f"Fin del procesamiento de la reserva {self.id}")

    def describir(self):
        return (f"Reserva #{self.id} | {self._cliente.nombre} | "
                f"{self._servicio.nombre} | {self._horas}h | {self._estado}")
