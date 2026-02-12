import pandas as pd
from typing import Tuple,  Any

from logs.loggers import start_logger
log = start_logger(__name__)

def verificar_existencia_entre_dfs(dict_series: dict[str, pd.Series]) -> Tuple[dict, bool]:
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