import pandas as pd
from typing import Tuple

from logs.loggers import start_logger
log = start_logger(__name__)

def _verificar_existencia_entre_dfs(dict_series: dict[str, pd.Series]) -> Tuple[dict, bool]:
    """
    Revisa que, entre 2 series de Pandas, el registro de la serie prioridad contenga todos los valores de la segunda serie

    Recibe:
    - Un diccionario con 2 series de Pandas que describe la prioridad en base a sus claves. Ej: {"prioridad": serie_1, "subprioridad": serie_2}

    Devuelve:
    - Un diccionario de errores 
    - Un valor booleano
    """
    df_prioridad = dict_series["prioridad"]
    df_subprioridad = dict_series["subprioridad"]

    faltantes = df_subprioridad[~df_subprioridad.isin(df_prioridad)]
    if not faltantes.empty:
        lista_faltantes = faltantes.tolist()
        log.error("Se han detectado faltantes en la serie de subprioridad -> Faltantes: %s")
        return {"faltantes_tabla_subprioridad": lista_faltantes}, False
    
    log.debug("Se verificó exitósamente la existencia de valores de la serie subprioritaria en la serie prioritaria")
    return {}, True


def _verificacion_nulos_negativos(s1: pd.Series) -> Tuple[dict, bool]:
    """
    Revisa que, en una serie de Pandas, no hayan valores nulos o negativos

    Recibe:
    - Una serie de Pandas

    Devuelve:
    - Un diccionario con los valores que fallaron la verificación
    - Un valor booleano
    """
    dict_errores = {}

    valores_nulos = s1[s1.isna()].tolist()
    valores_negativos =  s1[s1 < 0].tolist()
    
    if valores_nulos:
        log.error("Se han encontrado valores nulos dentro del DataFrame -> Valores nulos: %s", valores_nulos)
        dict_errores["valores_nulos"] = valores_nulos

    if valores_negativos:
        log.error("Se han encontrado valores negativos dentro del DataFrame -> Diccionario de errores: %s", dict_errores["valores_negativos"])
        dict_errores["valores_nulos"] = valores_nulos

    if dict_errores:
        return dict_errores, False

    log.debug("Verificado satisfactoriamente los valores nulos y negativos")
    return dict_errores, True


def verificar_dfs(dict_dfs: dict[str, pd.DataFrame]) -> Tuple[dict, bool]:
    """
    Realiza verificación de negativos y existencia entre 3 DataFrames ESPECÍFICOS

    Recibe un diccionario con:
    - DataFrame de recetas
    - DataFrame de ventas
    - DataFrame de stock

    Devuelve:
    - Un diccionario de errores
    - Un valor booleano
    """
    dict_errores = {}

    # Realizo verificaciones de nulos y valores negativos
    for df_name, df in dict_dfs.items():
        log.debug("Realizando la verificación de nulos y valores negativos -> DataFrame: %s", df_name)

        # Obtengo las columnas numéricas del DataFrame
        cols_numericas = df.select_dtypes(include="number").columns
        log.debug("Columnas numéricas del DataFrame detectadas -> Columnas: %s", cols_numericas.tolist())

        valores_negativos =  s1[s1 < 0].tolist()        # SIN TERMINAR
