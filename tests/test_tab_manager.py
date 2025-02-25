import unittest
import pandas as pd
from unittest.mock import patch
import sys
import os
from PyQt5.QtWidgets import QApplication

# Add the parent directory to the system path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.tab_manager import TabManager

class TestTabManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a QApplication instance
        cls.app = QApplication(sys.argv)

    def setUp(self):
        # Create a sample DataFrame for testing
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': [5, 4, 3, 2, 1],
            'C': [10, 20, 30, 40, 50]
        }
        self.df = pd.DataFrame(data)
        self.tab_manager = TabManager("test_file.csv", "csv", self.df)
        self.tab_manager.main_axis = 'A'
        self.tab_manager.selected_data = ['B', 'C']

    @patch('modules.data_visualizer.GraphConstructor.plot_selected_columns')
    def test_plot_selected_columns(self, mock_plot_selected_columns):
        # Call the function to be tested
        self.tab_manager.plot_selected_columns()

        # Check if the plot_selected_columns method was called with the correct arguments
        mock_plot_selected_columns.assert_called_once_with(self.df, ['A'], ['B', 'C'])

if __name__ == '__main__':
    unittest.main()
