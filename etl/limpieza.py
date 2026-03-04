import pandas as pd

from logs.loggers import start_logger
log = start_logger(__name__)

def _normalizar_strings_df(strings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza una normalizacion de espacios sin sentido y pasa a snake_case

    Recibe:
    - El sub-DataFrame de strings

    Devuelve:
    - El DataFrame "limpio"
    """
    strings_df = strings_df.apply(
        lambda col: (
            col.str.strip()
            .str.lower()
            .str.replace(r"\s+", "_", regex=True)
        )
    )
    return strings_df

def normalizar_dfs(dfs_dict: dict[str, pd.DataFrame], cols_pks: dict[str, str], dfs_metadata: dict[str, dict]) -> dict[str, pd.DataFrame]:
    """
    Realiza una limpieza de nulos en registros sin PK y conversión de strings a snake_case

    Recibe:
    - Un diccionario de DataFrames
    - Un diccionario con las PK de los DataFrames
    - Un diccionario con la metadata de los DataFrames (sus columnas y tipos de dato)

    Devuelve:
    - El mismo diccionario con los DataFrames normalizados
    """
    # Elimino PKs nulos y "mugre" en las celdas de DataFrames
    for df_name, df in dfs_dict.items():
        log.debug("Realizando limpieza de nulos y normalización de strings -> DataFrame : %s", df_name)

        # Obtengo columnas de strings
        obj_cols = [col for col, dtype in dfs_metadata[df_name].items() if dtype == "string"]
        log.debug("Columnas de strings obtenidas -> Columnas: %s", obj_cols)

        # Paso a snake_case las celdas, eliminando la "mugre"
        df[obj_cols] = _normalizar_strings_df(df[obj_cols])

        # Limpio nulos
        df_pk: str = cols_pks[df_name] # La clave del diccionario y la del archivo de configuración tiene que ser la misma (receta == receta)
        df_sin_na = df[df[df_pk].notna()]
        log.debug("Limpieza de nulos realizada -> Cantidad de nulos: %s", len(df) - len(df_sin_na))

        df = df_sin_na
    
    return dfs_dict