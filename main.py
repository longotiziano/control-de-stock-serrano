from utils import crear_dataframes, paso_snake_case
from validaciones.verificadores_datos import verificar_existencia_entre_dfs
from validaciones.verificadores_estructura import cargar_json, validar_columnas_df

from pathlib import Path

from logs.config import setup_logging
from logs.loggers import start_logger

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXCEL_VENTAS = DATA_DIR / "ventas" / "INFORME DE VENTAS 31-1-26 CLUB TN.xlsx"
EXCEL_STOCK = DATA_DIR / "control" / "control_de_stock.xlsx"
CONFIG_FILE = BASE_DIR / "validaciones" / "config.json"

if __name__ == "__main__":
    # Largo la configuración del logger
    setup_logging()
    log = start_logger(__name__)
    log.info("Logging configurado, iniciando programa...")

    # Paso los Excels a DataFrames. 
    dfs_dict, dfs_ok = crear_dataframes(EXCEL_VENTAS, EXCEL_STOCK)
    if not dfs_ok:
        raise ValueError("Ha habido un error durante la creación de DataFrames, por favor revisar los logs")
    log.info("Creación de DataFrames finalizada")

    # Pasado a minúsculas de columnas
    for _, df in dfs_dict.items():
        df.columns = paso_snake_case(df.columns.tolist())
        log.debug("Paso a snake_case exitoso -> Columnas: %s", df.columns.tolist())

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

    # Introducción al programa
    bar_name = input("Por favor, introduzca el nombre del bar: ").lower().strip()

    while not (bar_name in config_dicts["sucursales"]["lista_bares"]):
        bar_name = input(f'No se encontraron referencias para el bar "{bar_name}". Por favor, introduzca uno nuevamente: ').lower().strip()
    log.info(f'Valor ingresado correctamente, realizando conversión para el bar "{bar_name}"...')

    # Reducción de DataFrame en base al bar seleccionado
    df_recetas = df_recetas[df_recetas['bar'] == bar_name]
    df_stock = df_stock[df_stock['bar'] == bar_name]

    # Validaciones de existencia
    pass