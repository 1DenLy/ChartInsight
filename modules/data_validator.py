import pandas as pd

def validate_data(df):
    """
    Перевіряє, чи придатні дані для аналізу.
    
    :param df: pandas DataFrame
    :return: Кортеж (bool, список проблем)
    """
    issues = []

    if df is None or df.empty:
        issues.append("DataFrame порожній або не завантажений.")
    
    # Перевіряємо наявність хоча б однієї числової колонки
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) == 0:
        issues.append("Немає числових колонок для аналізу.")

    if issues:
        return False, issues
    return True, ["Дані пройшли перевірку."]

def convert_date_columns(df):
    """Convert all date columns to datetime format."""
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')


