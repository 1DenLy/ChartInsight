import pandas as pd
import os
from PyQt5.QtWidgets import QFileDialog
from modules.data_loader import populate_list_view

class FileManager:
    def __init__(self, window):
        self.window = window

    def save_to_file(self, df, file_path):
        """
        Save the DataFrame to a file.
        
        :param df: pandas DataFrame
        :param file_path: Path to the file
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
            print(f"Data successfully saved to {file_path}")
        except Exception as e:
            print(f"Error saving data to file: {e}")

    def load_from_file(self, file_path):
        """
        Load data from a file into a pandas DataFrame.
        
        :param file_path: Path to the file
        :return: DataFrame or None if an error occurs
        """
        try:
            df = pd.read_csv(file_path)
            print(f"Data successfully loaded from {file_path}")
            return df
        except Exception as e:
            print(f"Error loading data from file: {e}")
            return None

    def save_data_to_file(self):
        """Save the current DataFrame to a file."""
        if self.window.df is not None:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self.window, "Save to file", "data/", 
                                                       "CSV files (*.csv);;All Files (*)", options=options)
            if file_path:
                self.save_to_file(self.window.df, file_path)
        else:
            print("No data to save.")

    def load_data_from_file(self):
        """Load data from a file into the application."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Load from file", "data/", 
                                                   "CSV files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.window.df = self.load_from_file(file_path)
            if self.window.df is not None:
                populate_list_view(self.window.listWidget, self.window.df)
