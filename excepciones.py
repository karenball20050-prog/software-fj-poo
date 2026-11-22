"""Módulo de excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""

    def __init__(self, mensaje="Error en el sistema Software FJ"):
        # Guardamos el mensaje para poder mostrarlo o registrarlo después
        self.mensaje = mensaje
        # Llamamos al constructor de Exception para conservar el comportamiento estándar
        super().__init__(mensaje)


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los datos de un cliente no cumplen las validaciones."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando los parámetros de un servicio son incorrectos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta usar un servicio no disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta crear una reserva con datos incorrectos."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación no permitida en el estado actual."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos produce un resultado inconsistente."""
