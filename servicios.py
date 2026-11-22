"""Clase abstracta Servicio y tres servicios especializados."""

from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (ServicioInvalidoError, ParametroFaltanteError,
                         CalculoInconsistenteError)
from logger import log


class Servicio(EntidadBase):
    """Clase abstracta de la que heredan todos los servicios."""

    def __init__(self, identificador, nombre=None, tarifa_hora=None, disponible=True):
        # Validamos que los parámetros obligatorios existan
        if nombre is None or tarifa_hora is None:
            raise ParametroFaltanteError("Faltan nombre o tarifa del servicio")
        super().__init__(identificador)
        # Atributos protegidos (encapsulación)
        self._nombre = nombre
        self._tarifa_hora = tarifa_hora
        self._disponible = disponible
        # Cada hija define sus propias validaciones (polimorfismo)
        self.validar_parametros()

    @property
    def nombre(self):
        """Nombre del servicio."""
        return self._nombre

    @property
    def disponible(self):
        """Indica si el servicio puede reservarse."""
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        """Activa o desactiva el servicio."""
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self):
        """Valida los parámetros propios de cada servicio."""

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """Calcula el costo. Variantes por parámetros opcionales (sobrecarga)."""

    def _aplicar_ajustes(self, subtotal, impuesto, descuento):
        """Aplica descuento e impuesto a un subtotal y verifica consistencia."""
        # El impuesto y el descuento deben estar entre 0 y 1 (0% a 100%)
        if not (0 <= impuesto <= 1) or not (0 <= descuento <= 1):
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango [0,1]")
        # Primero descontamos y luego sumamos el impuesto
        total = subtotal * (1 - descuento) * (1 + impuesto)
        # Un costo no positivo indica un cálculo inconsistente
        if total <= 0:
            raise CalculoInconsistenteError(f"Costo calculado inconsistente: {total}")
        return round(total, 2)

    def _validar_horas(self, horas):
        """Comprueba que las horas sean un número positivo."""
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise CalculoInconsistenteError(f"Horas inválidas: {horas!r}")

    def _validar_tarifa(self):
        """Comprueba que la tarifa sea un número positivo."""
        if not isinstance(self._tarifa_hora, (int, float)) or self._tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {self._tarifa_hora!r}")

    @classmethod
    def crear(cls, *args, **kwargs):
        """Fábrica segura: crea el servicio y registra el resultado en el log."""
        try:
            servicio = cls(*args, **kwargs)
        except Exception as e:
            log.error(f"Fallo al crear servicio {cls.__name__}: {e}")
            raise
        else:
            log.info(f"Servicio creado: {servicio.describir()}")
            return servicio


class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(self, identificador, nombre=None, tarifa_hora=None, capacidad=None):
        # Guardamos primero la capacidad para que validar_parametros la encuentre
        self._capacidad = capacidad
        super().__init__(identificador, nombre, tarifa_hora)

    def validar_parametros(self):
        self._validar_tarifa()
        if not isinstance(self._capacidad, int) or self._capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {self._capacidad!r}")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_horas(horas)
        return self._aplicar_ajustes(self._tarifa_hora * horas, impuesto, descuento)

    def describir(self):
        return (f"Sala '{self.nombre}' (capacidad {self._capacidad}) "
                f"- ${self._tarifa_hora}/hora")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (el costo depende de la cantidad)."""

    def __init__(self, identificador, nombre=None, tarifa_hora=None, cantidad=None):
        self._cantidad = cantidad
        super().__init__(identificador, nombre, tarifa_hora)

    def validar_parametros(self):
        self._validar_tarifa()
        if not isinstance(self._cantidad, int) or self._cantidad <= 0:
            raise ServicioInvalidoError(f"Cantidad inválida: {self._cantidad!r}")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_horas(horas)
        # El costo se multiplica por la cantidad de equipos alquilados
        subtotal = self._tarifa_hora * horas * self._cantidad
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Equipo '{self.nombre}' x{self._cantidad} "
                f"- ${self._tarifa_hora}/hora c/u")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría; los expertos 'senior' tienen un recargo del 25%."""

    NIVELES = ("junior", "senior")  # Niveles permitidos

    def __init__(self, identificador, nombre=None, tarifa_hora=None, nivel=None):
        self._nivel = nivel
        super().__init__(identificador, nombre, tarifa_hora)

    def validar_parametros(self):
        self._validar_tarifa()
        if self._nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel inválido: {self._nivel!r}")

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        self._validar_horas(horas)
        subtotal = self._tarifa_hora * horas
        # Recargo del 25% para asesores senior
        if self._nivel == "senior":
            subtotal *= 1.25
        return self._aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return (f"Asesoría '{self.nombre}' nivel {self._nivel} "
                f"- ${self._tarifa_hora}/hora")
