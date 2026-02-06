from utils import crear_dataframes
from validaciones.verificadores_estructura import cargar_json, validar_columnas_df

from pathlib import Path

from logs.config import setup_logging
from logs.loggers import start_logger
log = start_logger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXCEL_VENTAS = DATA_DIR / "ventas" / "INFORME DE VENTAS 31-1-26 CLUB TN.xlsx"
EXCEL_STOCK = DATA_DIR / "control" / "control_de_stock.xlsx"
CONFIG_FILE = BASE_DIR / "validaciones" / "config.json"

if __name__ == "__main__":
    log.info("Iniciando programa...")

    # Largo la configuración del logger
    setup_logging()

    # Paso los Excels a DataFrames. 
    dfs_dict, dfs_ok = crear_dataframes(EXCEL_VENTAS, EXCEL_STOCK)
    if not dfs_ok:
        raise ValueError("Ha habido un error durante la creación de DataFrames, por favor revisar los logs")
    log.info("Creación de DataFrames finalizada")

    df_recetas = dfs_dict["recetas"]
    df_stock = dfs_dict["stock"]
    df_ventas = dfs_dict["ventas"]

    # Carga de archivo
    config_dicts, dict_ok = cargar_json(CONFIG_FILE)
    if not dict_ok:
        raise ValueError("Revisar porfavor el archivo JSON y la dirección proporcionada -> Dirección: %s", CONFIG_FILE)
    log.info("Carga del archivo JSON exitosa")

    # Validación de estructura de Excels
    dict_errores, validacion_ok = validar_columnas_df(dfs_dict, config_dicts["definicion_columnas"])
    if not validacion_ok:
        raise ValueError("Hubo un error durante la validación de los DataFrames -> Diccionario de errores: %s", dict_errores)
    log.info("DataFrames validados correctamente")

    # Introducción y comienzo de conversión
    bar_name = input("Por favor, introduzca el nombre del bar: ").lower()
    while bar_name not in [config_dicts["sucursales"]["lista_bares"]]:
        bar_name = input(f'No se encontraron referencias para el bar "{bar_name}". Por favor, introduzca uno nuevamente: ')
    log.info(f'Valor ingresado correctamente, realizando conversión para el bar "{bar_name}"...')
