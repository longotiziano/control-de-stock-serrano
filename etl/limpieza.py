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

def normalizar_dfs(dfs_dict: dict[str, pd.DataFrame], cols_pks: dict[str, str]) -> Tuple[dict[str, pd.DataFrame], bool]:
    """
    Realiza una limpieza de nulos en registros sin PK y conversión de strings a snake_case

    Recibe:
    - Un diccionario de DataFrames
    - Un diccionario con las columnas de las PK

    Devuelve:
    - El mismo diccionario con los DataFrames normalizados, o un diccionario de errores
    - Un valor booleano
    """
    # Elimino PKs nulos y "mugre" en las celdas de DataFrames
    for df_name, df in dfs_dict.items():
        log.debug("Realizando limpieza de nulos y normalización de strings -> DataFrame : %s", df_name)

        # Obtengo columnas de strings
        obj_cols = df.select_dtypes(include=["string"]).columns
        log.debug("Columnas de strings detectadas -> Columnas: %s", obj_cols.tolist())

        # Paso a snake_case las celdas, eliminando la "mugre"
        df[obj_cols] = _normalizar_strings_df(df[obj_cols])

        # Limpio nulos
        df_pk: str = cols_pks[df_name] # La clave del diccionario y la del archivo de configuración tiene que ser la misma (receta == receta)
        df_sin_na = df[df[df_pk].notna()]
        log.debug("Limpieza de nulos realizada -> Cantidad de nulos: %s", len(df) - len(df_sin_na))
    
    return 