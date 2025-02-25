import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic
import os

from modules.data_loader import load_data
from modules.data_validator import validate_data, convert_date_columns
from modules.window_manager import WindowManager
from modules.database_manager import FileManager
from modules.settings_manager import open_settings_tab
from modules.tab_manager import TabManager

class DataAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main_window.ui", self)

        self.window_manager = WindowManager(self)
        self.file_manager = FileManager(self)
        self.window_manager.load_window_settings()
        self.window_manager.load_and_set_icons()

        # Apply stylesheet
        #self.apply_stylesheet()

        # Connect buttons to their respective functions
        self.pushButton_open_file.clicked.connect(self.load_data_wrapper)
        #self.pushButton_plot.clicked.connect(self.plot_selected_columns)
        self.pushButton_save.clicked.connect(self.file_manager.save_data_to_file)
        self.pushButton_load.clicked.connect(self.file_manager.load_data_from_file)
        self.pushButton_settings.clicked.connect(lambda: open_settings_tab(self.tabWidget))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.window_manager.close_tab(index))

        self.current_fig = None
        self.df = None
        self.tab_managers = {}

    def apply_stylesheet(self):
        """Apply the stylesheet to the application."""
        with open("UI/style.qss", "r") as file:
            self.setStyleSheet(file.read())

    def resizeEvent(self, event):
        """Handle window resize event."""
        self.window_manager.resize_window(event)

    def closeEvent(self, event):
        """Handle window close event."""
        self.window_manager.save_window_settings()
        super().closeEvent(event)

    def load_data_wrapper(self):
        """Wrapper to call load_data and populate_list_view."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a file", "", 
                                                "CSV files (*.csv);;Excel files (*.xlsx);;JSON files (*.json)", options=options)
        if file_name:
            self.df = load_data(file_name)  # Load data

            if self.df is not None:
                is_valid, issues = validate_data(self.df)
                for issue in issues:
                    print(issue)  # Print validation messages

                if is_valid:
                    print(self.df.head())  # Print first few rows for verification
                    convert_date_columns(self.df)
                    self.create_new_tab(os.path.basename(file_name), file_name)

    def create_new_tab(self, tab_name, file_path):
        """Create a new tab with the new interface."""
        # Create a TabManager instance for the new tab
        file_format = os.path.splitext(file_path)[1][1:]
        tab_manager = TabManager(tab_name, file_format, self.df)
        self.tab_managers[tab_name] = tab_manager

        # Create the new tab using TabManager
        tab_manager.create_new_tab(self.tabWidget, tab_name, file_path)

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
