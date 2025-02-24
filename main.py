import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QListWidgetItem
from PyQt5 import uic
import os
import pandas as pd

from modules.data_loader import load_data
from modules.data_validator import validate_data
from modules.data_visualizer import plot_selected_columns, open_plot_in_window
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
        #self.pushButton_plot.clicked.connect(self.plot_selected_columns_wrapper)
        self.pushButton_open_plot.clicked.connect(self.open_plot_in_window_wrapper)
        self.pushButton_save.clicked.connect(self.file_manager.save_data_to_file)
        self.pushButton_load.clicked.connect(self.file_manager.load_data_from_file)
        self.pushButton_settings.clicked.connect(lambda: open_settings_tab(self.tabWidget))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.window_manager.close_tab(index))

        self.current_fig = None
        self.df = None
        self.tab_managers = {}
        self.hidden_items = {}

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
                    self.convert_date_columns(self.df)
                    self.create_new_tab(os.path.basename(file_name), file_name)

    def convert_date_columns(self, df):
        """Convert all date columns to datetime format."""
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

    def create_new_tab(self, tab_name, file_path):
        """Create a new tab with the new interface."""
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        new_interface = uic.loadUi("UI/new_tab.ui")
        layout.addWidget(new_interface.Frame_main)
        self.tabWidget.addTab(new_tab, tab_name)
        self.tabWidget.setCurrentWidget(new_tab)

        # Create a TabManager instance for the new tab
        file_format = os.path.splitext(file_path)[1][1:]
        tab_manager = TabManager(tab_name, file_format, self.df)
        self.tab_managers[tab_name] = tab_manager

        # Set label values
        tab_manager.set_label_values(new_interface)

        # Populate comboBox_main_ox with suitable columns for the main axis
        tab_manager.populate_main_axis_combobox(new_interface.comboBox_main_ox)
        new_interface.comboBox_main_ox.insertItem(0, "Select Main Axis")
        new_interface.comboBox_main_ox.setCurrentIndex(0)

        # Populate list_all_data with columns from the dataset
        self.populate_list_all_data(new_interface.list_all_data, tab_manager.data_columns)

        # Connect double-click event to move items between lists
        new_interface.list_all_data.itemDoubleClicked.connect(lambda item: self.move_item_between_lists(item, new_interface.list_all_data, new_interface.list_changed_data, new_interface.comboBox_main_ox.currentText()))
        new_interface.list_changed_data.itemDoubleClicked.connect(lambda item: self.move_item_between_lists(item, new_interface.list_changed_data, new_interface.list_all_data, new_interface.comboBox_main_ox.currentText()))

        # Connect comboBox_main_ox change event to update lists
        new_interface.comboBox_main_ox.currentIndexChanged.connect(lambda: self.update_lists(new_interface))

    def populate_list_all_data(self, list_widget, data_columns):
        """Populate the list widget with columns from the dataset."""
        list_widget.clear()
        for col in data_columns:
            item = QListWidgetItem(col['name'])
            list_widget.addItem(item)

    def move_item_between_lists(self, item, source_list, target_list, main_axis):
        """Move item between lists, excluding the main axis."""
        if item.text() != main_axis:
            source_list.takeItem(source_list.row(item))
            target_list.addItem(item.text())

    def update_lists(self, interface):
        """Update the lists to exclude the selected main axis."""
        main_axis = interface.comboBox_main_ox.currentText()
        current_tab = self.tabWidget.currentWidget()
        tab_manager = self.tab_managers[self.tabWidget.tabText(self.tabWidget.indexOf(current_tab))]
        self.populate_list_all_data(interface.list_all_data, tab_manager.data_columns)
        self.hide_main_axis_in_lists(interface, main_axis)

    def hide_main_axis_in_lists(self, interface, main_axis):
        """Hide the selected main axis from the lists and show previously hidden items."""
        if main_axis in self.hidden_items:
            for item in self.hidden_items[main_axis]:
                interface.list_all_data.addItem(item)
            del self.hidden_items[main_axis]

        self.hidden_items[main_axis] = []
        for i in range(interface.list_all_data.count()):
            item = interface.list_all_data.item(i)
            if item and item.text() == main_axis:
                self.hidden_items[main_axis].append(item.text())
                interface.list_all_data.takeItem(i)
                i -= 1

        for i in range(interface.list_changed_data.count()):
            item = interface.list_changed_data.item(i)
            if item and item.text() == main_axis:
                self.hidden_items[main_axis].append(item.text())
                interface.list_changed_data.takeItem(i)
                i -= 1

    def open_plot_in_window_wrapper(self):
        """Wrapper to call open_plot_in_window with the current figure."""
        open_plot_in_window(self.current_fig)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
