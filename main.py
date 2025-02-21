import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog
from PyQt5 import uic

from modules.data_loader import load_data, populate_list_view
from modules.data_validator import validate_data
from modules.data_visualizer import plot_selected_columns, open_plot_in_window
from modules.window_manager import save_window_settings, load_window_settings, close_tab, resize_window
from modules.database_manager import save_data_to_database, load_data_from_database

class DataAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main_window.ui", self)
        load_window_settings(self)

        # Connect buttons to their respective functions
        self.pushButton_open_file.clicked.connect(self.load_data_wrapper)

        self.pushButton_x_axis.clicked.connect(self.select_x_axis)
        self.pushButton_y_axis.clicked.connect(self.select_y_axis)

        self.pushButton_plot.clicked.connect(self.plot_selected_columns_wrapper)
        self.pushButton_open_plot.clicked.connect(self.open_plot_in_window_wrapper)
        
        self.pushButton_save.clicked.connect(lambda: save_data_to_database(self))
        self.pushButton_load.clicked.connect(lambda: load_data_from_database(self))
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(lambda index: close_tab(self, index))

        self.current_fig = None
        self.df = None

    def resizeEvent(self, event):
        """Handle window resize event."""
        resize_window(self, event)

    def closeEvent(self, event):
        """Handle window close event."""
        save_window_settings(self)
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
                    populate_list_view(self.listWidget, self.df)

    def select_x_axis(self):
        """Select the column for the x-axis."""
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            if item.text() not in [self.listWidget_x_axis.item(i).text() for i in range(self.listWidget_x_axis.count())]:
                self.listWidget_x_axis.addItem(item.text())
            else:
                for i in range(self.listWidget_x_axis.count()):
                    if self.listWidget_x_axis.item(i).text() == item.text():
                        self.listWidget_x_axis.takeItem(i)
                        break

    def select_y_axis(self):
        """Select the column for the y-axis."""
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            if item.text() not in [self.listWidget_y_axis.item(i).text() for i in range(self.listWidget_y_axis.count())]:
                self.listWidget_y_axis.addItem(item.text())
            else:
                for i in range(self.listWidget_y_axis.count()):
                    if self.listWidget_y_axis.item(i).text() == item.text():
                        self.listWidget_y_axis.takeItem(i)
                        break

    def plot_selected_columns_wrapper(self):
        """Wrapper to call plot_selected_columns with the correct parameters."""
        x_cols = [self.listWidget_x_axis.item(i).text() for i in range(self.listWidget_x_axis.count())]
        y_cols = [self.listWidget_y_axis.item(i).text() for i in range(self.listWidget_y_axis.count())]
        self.current_fig = plot_selected_columns(self.df, x_cols, y_cols, self.tabWidget)

    def open_plot_in_window_wrapper(self):
        """Wrapper to call open_plot_in_window with the current figure."""
        open_plot_in_window(self.current_fig)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
