import pandas as pd


def validate_data(df):
    """
    Перевіряє, чи придатні дані для аналізу.
    
    :param df: pandas DataFrame
    :return: Кортеж (bool, список проблем)
    """
    issues = []

    if df is None or df.empty:
        issues.append("❌ DataFrame порожній або не завантажений.")
    
    # Перевіряємо наявність хоча б однієї числової колонки
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) == 0:
        issues.append("❌ Немає числових колонок для аналізу.")

    # Перевіряємо наявність пропущених значень
    missing_values = df.isnull().sum().sum()
    if missing_values > 0:
        issues.append(f"⚠️ У даних є {missing_values} пропущених значень.")
    
    # Перевіряємо наявність дублікатів
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        issues.append(f"⚠️ У даних є {duplicate_rows} дублікатів.")

    if issues:
        return False, issues
    return True, ["✅ Дані пройшли перевірку."]

