"""Simulación de 12 operaciones: válidas e inválidas. El programa nunca se detiene."""

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import ErrorSoftwareFJ
from logger import log


def ejecutar(numero, titulo, operacion):
    """Ejecuta una operación aislada: si falla, se registra y el programa sigue."""
    print(f"\n[{numero:02d}] {titulo}")
    try:
        resultado = operacion()          # Ejecutamos la operación recibida
    except ErrorSoftwareFJ as e:
        # Error controlado del sistema: se registra en el log (garantiza que todo error quede guardado)
        log.error(f"Operación {numero} ({titulo}) falló: {type(e).__name__}: {e}")
        print(f"   ERROR CONTROLADO ({type(e).__name__}): {e}")
        if e.__cause__:                   # Mostramos la causa si hubo encadenamiento
            print(f"   Causa original: {e.__cause__!r}")
    except Exception as e:
        # Cualquier otro error imprevisto
        log.critical(f"Error no previsto en operación {numero}: {e}")
        print(f"   ERROR INESPERADO ({type(e).__name__}): {e}")
    else:
        print(f"   OK -> {resultado}")
        return resultado


def main():
    log.info("===== INICIO DE LA SIMULACIÓN =====")

    # 1. Cliente válido
    cliente = ejecutar(1, "Cliente válido", lambda: Cliente.crear(
        1, "Laura Gómez", "laura@correo.com", "3001234567"))
    # 2. Correo inválido
    ejecutar(2, "Cliente con correo inválido", lambda: Cliente.crear(
        2, "Pedro Ruiz", "pedro-correo", "3109876543"))
    # 3. Nombre vacío
    ejecutar(3, "Cliente con nombre vacío", lambda: Cliente.crear(
        3, "  ", "x@correo.com", "3109876543"))
    # 4. Teléfono no numérico (demuestra encadenamiento)
    ejecutar(4, "Cliente con teléfono no numérico", lambda: Cliente.crear(
        4, "Ana Torres", "ana@correo.com", "abc123"))
    # 5. Parámetro faltante
    ejecutar(5, "Cliente sin correo ni teléfono", lambda: Cliente.crear(5, "Sin Datos"))

    # 6. Servicios válidos
    sala = ejecutar(6, "Servicio válido: sala", lambda: ReservaSala.crear(
        101, "Sala Ejecutiva", 50000, 12))
    equipo = ejecutar(7, "Servicio válido: equipo", lambda: AlquilerEquipo.crear(
        102, "Videobeam", 20000, 3))
    asesoria = ejecutar(8, "Servicio válido: asesoría", lambda: AsesoriaEspecializada.crear(
        103, "Asesoría en Python", 80000, "senior"))
    # 9. Servicio con tarifa negativa
    ejecutar(9, "Servicio con tarifa negativa", lambda: ReservaSala.crear(
        104, "Sala Rota", -100, 5))

    # 10. Reserva exitosa
    reserva1 = ejecutar(10, "Reserva válida", lambda: Reserva(1, cliente, sala, 3))
    if reserva1:
        ejecutar(11, "Procesar reserva con 19% IVA y 10% descuento",
                 lambda: reserva1.procesar(impuesto=0.19, descuento=0.10))
        # 12. Cancelar dos veces la misma reserva
        ejecutar(12, "Cancelar reserva", reserva1.cancelar)
        ejecutar(13, "Cancelar de nuevo (no permitido)", reserva1.cancelar)

    # 14. Duración cero
    ejecutar(14, "Reserva con duración 0", lambda: Reserva(2, cliente, equipo, 0))
    # 15. Servicio no disponible
    equipo.cambiar_disponibilidad(False)
    reserva3 = ejecutar(15, "Reserva sobre equipo no disponible",
                        lambda: Reserva(3, cliente, equipo, 2))
    if reserva3:
        ejecutar(16, "Procesar reserva de servicio no disponible", reserva3.procesar)
    # 17. Cliente inexistente
    ejecutar(17, "Reserva sin cliente", lambda: Reserva(4, None, sala, 2))
    # 18. Variantes de cálculo de costo (sobrecarga con parámetros opcionales)
    ejecutar(18, "Costos asesoría: simple / con IVA / con IVA y descuento",
             lambda: (asesoria.calcular_costo(2),
                      asesoria.calcular_costo(2, 0.19),
                      asesoria.calcular_costo(2, 0.19, 0.15)))
    # 19. Descuento fuera de rango
    ejecutar(19, "Cálculo con descuento 150%", lambda: sala.calcular_costo(2, 0.19, 1.5))

    # Polimorfismo: misma llamada, distinto comportamiento
    print("\n--- Polimorfismo: describir() de cada servicio ---")
    for s in (sala, equipo, asesoria):
        print("  ", s.describir())

    log.info("===== FIN DE LA SIMULACIÓN =====")
    print("\nSimulación terminada sin interrupciones. Revisa logs.txt")


if __name__ == "__main__":
    main()
