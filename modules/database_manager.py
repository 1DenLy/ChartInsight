import sqlite3
import pandas as pd
import os
from PyQt5.QtWidgets import QFileDialog, QInputDialog
from modules.data_loader import populate_list_view

def save_to_database(df, db_path, table_name):
    """
    Save the DataFrame to an SQLite database.
    
    :param df: pandas DataFrame
    :param db_path: Path to the SQLite database file
    :param table_name: Name of the table to save the data
    """
    try:
        create_database_if_not_exists(db_path)
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Data successfully saved to {table_name} in {db_path}")
    except Exception as e:
        print(f"Error saving data to database: {e}")

def load_from_database(db_path, table_name):
    """
    Load data from an SQLite database into a pandas DataFrame.
    
    :param db_path: Path to the SQLite database file
    :param table_name: Name of the table to load the data from
    :return: DataFrame or None if an error occurs
    """
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        print(f"Data successfully loaded from {table_name} in {db_path}")
        return df
    except Exception as e:
        print(f"Error loading data from database: {e}")
        return None

def create_database_if_not_exists(db_path):
    """
    Create a new SQLite database if it does not exist.
    
    :param db_path: Path to the SQLite database file
    """
    os.makedirs(os.path.join('data', os.path.dirname(db_path)), exist_ok=True)
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"Database created at {db_path}")

def save_data_to_database(window):
    """Save the current DataFrame to an SQLite database."""
    if window.df is not None:
        options = QFileDialog.Options()
        db_path, _ = QFileDialog.getSaveFileName(window, "Save to database", "data/", 
                                                 "SQLite Database (*.sqlite);;All Files (*)", options=options)
        if db_path:
            create_database_if_not_exists(db_path)
            table_name, ok = QInputDialog.getText(window, "Table Name", "Enter the table name:")
            if ok and table_name:
                save_to_database(window.df, db_path, table_name)
    else:
        print("No data to save.")

def load_data_from_database(window):
    """Load data from an SQLite database into the application."""
    options = QFileDialog.Options()
    db_path, _ = QFileDialog.getOpenFileName(window, "Load from database", "data/", 
                                             "SQLite Database (*.sqlite);;All Files (*)", options=options)
    if db_path:
        table_name, ok = QInputDialog.getText(window, "Table Name", "Enter the table name:")
        if ok and table_name:
            window.df = load_from_database(db_path, table_name)
            if window.df is not None:
                populate_list_view(window.listWidget, window.df)
