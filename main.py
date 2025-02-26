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
        self.pushButton_plot.clicked.connect(self.plot_active_tab)
        self.pushButton_save.clicked.connect(self.file_manager.save_data_to_file)
        self.pushButton_load.clicked.connect(self.load_data_from_file)
        self.pushButton_settings.clicked.connect(lambda: open_settings_tab(self.tabWidget))
        self.pushButton_open_plot.clicked.connect(self.open_last_plot)
        self.pushButton_data_update.clicked.connect(self.update_data_from_file)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.window_manager.close_tab(index))

        self.current_fig = None
        self.df = None
        self.tab_managers = {}
        self.last_plot = None  # Temporary variable to store the last created plot

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

    def load_data_from_file(self):
        """Load data from a file into the application."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Load from file", "data/", 
                                                   "CSV files (*.csv);;Excel files (*.xlsx);;JSON files (*.json);;All Files (*)", options=options)
        if file_path:
            self.df = load_data(file_path)  # Load data

            if self.df is not None:
                is_valid, issues = validate_data(self.df)
                for issue in issues:
                    print(issue)  # Print validation messages

                if is_valid:
                    print(self.df.head())  # Print first few rows for verification
                    convert_date_columns(self.df)
                    self.create_new_tab(os.path.basename(file_path), file_path)

    def create_new_tab(self, tab_name, file_path):
        """Create a new tab with the new interface."""
        # Create a TabManager instance for the new tab
        file_format = os.path.splitext(file_path)[1][1:]
        tab_manager = TabManager(tab_name, file_format, self.df)
        self.tab_managers[tab_name] = tab_manager

        # Create the new tab using TabManager
        tab_manager.create_new_tab(self.tabWidget, tab_name, file_path)

    def plot_active_tab(self):
        """Plot the selected columns for the active tab."""
        current_tab_index = self.tabWidget.currentIndex()
        if current_tab_index != -1:
            tab_name = self.tabWidget.tabText(current_tab_index)
            if (tab_name in self.tab_managers):
                tab_manager = self.tab_managers[tab_name]
                self.last_plot = tab_manager.plot_selected_columns()  # Save the plot to the temporary variable

    def open_last_plot(self):
        """Open the last created plot."""
        if self.last_plot:
            self.last_plot.show()
        else:
            print("No plot available to open.")

    def update_data_from_file(self):
        """Update data from the currently opened file."""
        if self.df is not None:
            file_path = self.df.attrs.get('file_path')
            if file_path:
                self.df = load_data(file_path)  # Reload data
                if self.df is not None:
                    is_valid, issues = validate_data(self.df)
                    for issue in issues:
                        print(issue)  # Print validation messages

                    if is_valid:
                        print(self.df.head())  # Print first few rows for verification
                        convert_date_columns(self.df)
                        current_tab_index = self.tabWidget.currentIndex()
                        if current_tab_index != -1:
                            tab_name = self.tabWidget.tabText(current_tab_index)
                            if tab_name in self.tab_managers:
                                tab_manager = self.tab_managers[tab_name]
                                tab_manager.df = self.df  # Update the DataFrame in TabManager
                                tab_manager.data_columns = tab_manager.get_data_columns()  # Update data columns
                                tab_widget = self.tabWidget.widget(current_tab_index)
                                tab_manager.set_label_values(tab_widget)  # Update labels
                                tab_manager.populate_main_axis_combobox(tab_manager.logic_manager.comboBox_main_ox)  # Update comboBox
                                tab_manager.populate_list_all_data(tab_manager.logic_manager.list_all_data, tab_manager.data_columns)  # Update list
                                print("Data updated successfully.")
            else:
                print("No file path found in the DataFrame attributes.")
        else:
            print("No data to update.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
