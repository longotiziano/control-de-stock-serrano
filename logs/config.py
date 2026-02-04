import os
from pathlib import Path
import logging.config 

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_LOG_FILE = BASE_DIR / "logs" / "logs.csv"

# Creo el .csv en el cual se guardarán los logs
if not os.path.exists(CSV_LOG_FILE):
    with open(CSV_LOG_FILE, "w", newline="") as f:
        f.write('"timestamp","logger","level","message"\n')

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # No desactiva loggers ya existentes
    "formatters": {
        "csv": {
            "format": '"%(asctime)s","%(name)s","%(levelname)s","%(message)s"'
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {  # Handler que imprime en consola
            "class": "logging.StreamHandler",
            "formatter": "detailed",  # Usa el formatter definido arriba
            "level": "DEBUG",  # Nivel mínimo que se imprime en consola
        },
        "csv_file": {  # Handler que escribe en archivo
            "class": "logging.FileHandler",
            "formatter": "csv",
            "filename": str(CSV_LOG_FILE),
            "level": "DEBUG",
            "mode": "a",
        },
    },
    "root": {  # Logger raíz, abarca todo el proyecto
        "handlers": ["console", "csv_file"],
        "level": "DEBUG"
    }
}

def setup_logging() -> None:
    """
    Sets up logger initial configuration
    """
    logging.config.dictConfig(LOGGING_CONFIG)