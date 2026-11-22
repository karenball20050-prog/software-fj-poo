"""Módulo de registro (logs) de eventos y errores en el archivo logs.txt."""

import logging  # Módulo estándar de Python para registrar eventos
import os       # Para construir la ruta del archivo de logs

# Ruta del archivo de logs: queda junto a este módulo
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs.txt")


def obtener_logger():
    """Crea (una sola vez) y devuelve el logger del sistema."""
    # Obtenemos un logger con nombre propio
    logger = logging.getLogger("SoftwareFJ")
    # Si ya tiene manejadores, ya fue configurado: lo devolvemos tal cual
    if logger.handlers:
        return logger
    # Registramos todos los niveles (INFO, WARNING, ERROR...)
    logger.setLevel(logging.INFO)
    # Manejador que escribe en el archivo (mode="a" agrega al final)
    manejador = logging.FileHandler(RUTA_LOG, mode="a", encoding="utf-8")
    # Formato de cada línea: fecha, nivel y mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    manejador.setFormatter(formato)
    # Asociamos el manejador al logger
    logger.addHandler(manejador)
    return logger


# Logger único que importan los demás módulos
log = obtener_logger()
