import pandas as pd

def limpiar_strings(strings_df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza una limpieza de espacios sin sentido y pasa a snake_case

    Recibe:
    - El sub-DataFrame de strings

    Devuelve:
    - El DataFrame "limpio"
    """
    strings_df = (
    strings_df
    .apply(lambda col: col.str.strip())
    .apply(lambda col: col.str.lower())
    .apply(lambda col: col.str.replace(r"\s+", "_", regex=True))
    )

    return strings_df

def eliminar_pk_nulas(df: pd.DataFrame, pk: str) -> pd.DataFrame: ...