def main():
    from etl.limpieza import normalizar_dfs
    from utils import crear_dataframes, paso_snake_case
    from etl.verificadores_datos import verificar_dfs
    from etl.verificadores_estructura import cargar_json, validar_columnas_df, asignar_datatypes

    from pathlib import Path

    from logs.config import setup_logging
    from logs.loggers import start_logger

    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    EXCEL_VENTAS = DATA_DIR / "ventas" / "excel-test.xlsx"
    EXCEL_STOCK = DATA_DIR / "control" / "control_de_stock.xlsx"
    CONFIG_FILE = BASE_DIR / "validaciones" / "config.json"

    # Largo la configuración del logger
    setup_logging()
    log = start_logger(__name__)
    log.info("Logging configurado, iniciando programa...")

    # Paso los Excels a DataFrames. 
    dfs_dict, dfs_ok = crear_dataframes(EXCEL_VENTAS, EXCEL_STOCK)
    if not dfs_ok:
        raise ValueError("Ha habido un error durante la creación de DataFrames, por favor revisar los logs")
    log.info("Creación de DataFrames finalizada")

    # Pasado a snake_case de columnas
    for _, df in dfs_dict.items():
        df.columns = [paso_snake_case(col) for col in df.columns]
        log.debug("Paso a snake_case exitoso -> Columnas: %s", df.columns.tolist())

    # Carga de archivo
    config_dicts, dict_ok = cargar_json(CONFIG_FILE)
    if not dict_ok:
        raise ValueError("Revisar porfavor el archivo JSON y la dirección proporcionada -> Dirección: %s", CONFIG_FILE)
    log.info("Carga del archivo JSON exitosa")

    # Validación de estructura de Excels
    dict_errores, validacion_ok = validar_columnas_df(dfs_dict, config_dicts["datasets"])
    if not validacion_ok:
        raise ValueError("Hubo un error durante la validación de los DataFrames -> Diccionario de errores: %s", dict_errores)
    log.info("DataFrames validados correctamente")

    # Normalización de DataFrames -> Eliminación de nulos y pasado a snake_case
    dfs_dict = normalizar_dfs(dfs_dict, config_dicts["primary_keys"], config_dicts["datasets"]) # No cuido errores porque no tiene por qué haber

    # Asignación de tipos de dato
    dfs_dics = asignar_datatypes(dfs_dict, config_dicts["datasets"])

    # Introducción al programa
    bar_name = input("Por favor, introduzca el nombre del bar: ").lower().strip()

    while not (bar_name in config_dicts["sucursales"]["lista_bares"]):
        bar_name = input(f'No se encontraron referencias para el bar {bar_name}. Por favor, introduzca uno nuevamente: ').lower().strip()
    log.info(f'Valor ingresado correctamente, realizando conversión para el bar {bar_name}...')

    # Reducción de DataFrame en base al bar seleccionado
    dfs_dict["recetas"] = dfs_dict["recetas"][dfs_dict["recetas"]['bar'] == bar_name]
    dfs_dict["stock"] = dfs_dict["stock"][dfs_dict["stock"]['bar'] == bar_name]

    # Verificación de negativos y de existencia entre DataFrames para el correcto análisis
    # dict_errores, dfs_ok = verificar_dfs(dfs_dict)

if __name__ == "__main__":
    main()
    