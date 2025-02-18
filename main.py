import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTabWidget, QWidget, QVBoxLayout
from PyQt5 import uic
import pyqtgraph as pg

from modules.data_loader import load_data
from modules.data_validator import validate_data

class DataAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/main_window.ui", self)

        self.loadButton.clicked.connect(self.load_data)
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)

    def load_data(self):
        """Function to select and load a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select a file", "", 
                                                "CSV files (*.csv);;Excel files (*.xlsx);;JSON files (*.json)", options=options)
        if file_name:
            self.df = load_data(file_name)  # Load data

            if self.df is not None:
                is_valid, issues = validate_data(self.df)
                for issue in issues:
                    print(issue)  # Виводимо повідомлення про перевірку

                if is_valid:
                    print(self.df.head())  # Виводимо перші рядки для перевірки
                    self.create_new_tab(file_name)

    def create_new_tab(self, title):
        """Create a new tab with a plot."""
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        plot_widget = pg.PlotWidget()
        layout.addWidget(plot_widget)
        self.tabWidget.addTab(new_tab, title)
        self.tabWidget.setCurrentWidget(new_tab)

        # Example plot, you can customize it based on your data
        plot_widget.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
