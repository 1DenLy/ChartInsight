import pandas as pd
from PyQt5.QtWidgets import QListWidgetItem

def load_data(file_path):
    """
    Loads data from a file into a pandas DataFrame.
    
    :param file_path: Path to the file (CSV, Excel, JSON)
    :return: DataFrame or None if an error occurs
    """
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".json"):
            df = pd.read_json(file_path)
        else:
            print("Unsupported file format.")
            return None

        print(f"File successfully loaded: {file_path}")
        print(f"Data shape: {df.shape}")  # Displays (rows, columns)
        return df

    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def populate_list_view(list_widget, df):
    """Populate the list view with column names."""
    list_widget.clear()
    for col in df.columns:
        item = QListWidgetItem(col)
        list_widget.addItem(item)

