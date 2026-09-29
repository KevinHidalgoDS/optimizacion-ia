import pandas as pd


def clean_transactions(df: pd.DataFrame, threshold: float = 0.0) -> pd.DataFrame:
    """
    Filtra transacciones por debajo de un umbral monetario y elimina nulos.

    Args:
        df (pd.DataFrame): DataFrame crudo con el historial de transacciones.
        threshold (float): Valor mínimo permitido para la transacción.

    Returns:
        pd.DataFrame: DataFrame limpio y filtrado.

    Raises:
        ValueError: Si la columna 'monto' no existe en el DataFrame.
    """
    if "monto" not in df.columns:
        raise ValueError("El DataFrame debe contener la columna 'monto'")

    return df[df["monto"] >= threshold].dropna()
