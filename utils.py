import pandas as pd
from typing import Tuple

from logs.loggers import start_logger
log = start_logger(__name__)

def restaurantes_existentes():
    pass

def crear_dataframes(excel_ventas: str, excel_stock: str) -> Tuple[dict | None, bool]:
    """
    Recibe:
    - Ubicación del Excel de ventas
    - Ubicación del Excel de stock
    Devuelve:
    - DataFrame de recetas
    - DataFrame de stock
    - DataFrame de ventas
    """
    dataframes_dict = {}

    try:
        sheets = pd.read_excel(excel_stock, sheet_name=None, engine="openpyxl") 
        dataframes_dict["df_ventas"] = pd.read_excel(excel_ventas, engine="openpyxl")
        log.debug("Ambos archivos encontrados")

    except FileNotFoundError:
        log.error("Error durante la búsqueda del Excel, porfavor revisar dirección/nombre del archivo")
        return None, False

    try:
        dataframes_dict["df_recetas"] = sheets["Recetas"] # Importante que los nombres de las hojas coincidan
        dataframes_dict["df_stock"] = sheets["Stock"]
        log.debug("Identificación de hojas exitosa")

    except KeyError:
        log.error("Error al identificar las hojas dentro del Excel de stock, porfavor revisar coincidencia de nombres")
        return None, False
    
    return dataframes_dict, True