import pandas as pd
from pathlib import Path
from typing import Tuple

from logs.loggers import start_logger
log = start_logger(__name__)

def crear_dataframes(excel_ventas: Path, excel_stock: Path) -> Tuple[dict[str, pd.DataFrame], bool]:
    """
    Recibe:
    - Ubicación del Excel de ventas
    - Ubicación del Excel de stock

    Devuelve un diccionario con:
    - DataFrame de recetas
    - DataFrame de stock
    - DataFrame de ventas (o un diccionario vacío en caso de error)

    IMPORTANTE: al momento de nombrar las claves del diccionario retornado, es importante que se llamen IGUAL a las de columnas.json!!!
    """
    dataframes_dict = {}

    try:
        sheets = pd.read_excel(excel_stock, sheet_name=None, engine="openpyxl") 
        dataframes_dict["ventas"] = pd.read_excel(excel_ventas, engine="openpyxl")
        log.debug("Ambos archivos encontrados")

    except FileNotFoundError:
        log.error("Error durante la búsqueda del Excel, porfavor revisar dirección/nombre del archivo")
        return {}, False

    try:
        dataframes_dict["recetas"] = sheets["Recetas"] # Importante que los nombres de las hojas coincidan
        dataframes_dict["stock"] = sheets["Stock"]
        log.debug("Identificación de hojas exitosa")

    except KeyError:
        log.error("Error al identificar las hojas dentro del Excel de stock, porfavor revisar coincidencia de nombres")
        return {}, False
    
    return dataframes_dict, True