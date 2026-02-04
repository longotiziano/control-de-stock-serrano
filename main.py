from utils import crear_dataframes

from pathlib import Path

from logs.config import setup_logging
from logs.loggers import start_logger
log = start_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXCEL_VENTAS = DATA_DIR / "ventas" / "INFORME DE VENTAS 31-1-26 CLUB TN.xlsx"
EXCEL_STOCK = DATA_DIR / "control" / "control_de_stock.xlsx"

if __name__ == "__main__":
    log.info("Iniciando programa...")

    # Largo la configuración del logger
    setup_logging()

    # Paso los Excels a DataFrames. 
    dfs_dict, dfs_ok = crear_dataframes(EXCEL_VENTAS, EXCEL_STOCK)
    if not dfs_ok:
        raise ValueError("Ha habido un error durante la creación de DataFrames, por favor revisar los logs")
    log.info("Creación de DataFrames finalizada")

    # Validación de estructura de Excels

    # 
    bar_name = input("Por favor, introduzca el nombre del bar: ")
    while bar_name not in []:
        pass
