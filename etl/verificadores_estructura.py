import json
import pandas as pd
from pathlib import Path
from typing import Tuple, Any

from logs.loggers import start_logger
log = start_logger(__name__)

def cargar_json(json_file: Path) -> Tuple[dict[str, Any], bool]:
    """
    ### Recibe:
    - Un JSON
    ### Devuelve:
    - El diccionario cargado, o uno vacío
    - Un valor booleano
    """
    try:
        with open(json_file, "r", encoding="utf-8") as j:
            dict_ = json.load(j)

    except FileNotFoundError:
        log.error("Error al leer la dirección del JSON -> JSON: %s", json_file)
        return {}, False
    
    log.debug("Archivo JSON leído correctamente -> JSON: %s", json_file )    
    return dict_, True

def validar_columnas_df(dfs_dict: dict[str, pd.DataFrame], columns_dict: dict[str, dict]) -> Tuple[dict, bool]:
    """
    Valida que las columnas de los DataFrames coincidan con las columnas establecidas en el diccionario proporcionado

    ### Recibe:
    - Un diccionario con:
        - DataFrame de stock
        - DataFrame de recetas
        - DataFrame de ventas
    - Un diccionario de la configuración de los datasets
    ### Devuelve:
    - Diccionario con cada DataFrame y las columnas faltantes
    - Valor booleano

    PD: Cada uno de estos DataFrames tienen la MISMA clave que el archivo JSON (consultar utils.py)
    """
    errores = {}

    for nombre_df, df in dfs_dict.items():
        log.debug("Validando columnas y existencia dentro del JSON -> DataFrame: %s", nombre_df)

        if nombre_df in columns_dict:
            faltantes = set(columns_dict[nombre_df].keys()) - set(df.columns) # Una genialidad de los sets!
            if faltantes:
                errores[nombre_df] = list(faltantes)
        
        # En caso de que las claves en el JSON no coincidan con las del diccionario de DataFrames
        else:
            log.error("No pudimos encontrar coincidencias en el JSON para el DataFrame proporcionado en el diccionario -> Clave: %s", nombre_df)
            errores[nombre_df] = "No fue encontrado en el archivo JSON" 

    if errores:
        log.error("Se detectaron errores a la hora de validar los DataFrames -> Errores: %s", errores)
        return errores, False
    
    # No loggeo éxito porque lo loggeo con log.info() en el main.py
    return {}, True

def asignar_datatypes(dfs_dict: dict[str, pd.DataFrame], columns_dict: dict[str, dict]) -> Tuple[dict[str, Any], bool]:
    """
    Asigna los los tipos de datos a las respectivas columnas en los Excel.

    ### Recibe:
    - Un diccionario con:
        - DataFrame de stock
        - DataFrame de recetas
        - DataFrame de ventas
    - Un diccionario de la configuración de los datasets
    ### Devuelve:
    - El mismo diccionario con los datatypes asignados, o un diccionario de errores
    - Valor booleano
    """
    errores = {}

    for df_name, df in dfs_dict.items():
        df[] # LO DEJE aca