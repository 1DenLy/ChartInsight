import os
import math

from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QVBoxLayout
from PyQt5 import uic
from modules.logic_manager import LogicManager
from modules.data_visualizer import GraphConstructor

class TabManager:
    def __init__(self, file_name, file_format, df):
        self.file_name = file_name
        self.file_format = file_format
        self.df = df
        self.main_axis = None
        self.selected_data = []
        self.data_columns = self.get_data_columns()
        self.analysis_options = {
            "trend_line": False,
            "median": False,
            "average": False,
            "min_max": False,
            "moving_average": False,
            "sorting_main_axis": False,
            "sorting_values_graph": False,
            "filling_in_blank_values_average": False,
            "replacing_emissions": False,
            "delete_repetitions": False,
            "decomposition": False
        }
        self.file_size = self.get_file_size()
        self.missing_values_count = self.get_missing_values_count()
        self.outliers_count = self.get_outliers_count()
        self.logic_manager = LogicManager()

    def get_data_columns(self):
        """Get all detected data columns with their types and names."""
        columns = []
        for col in self.df.columns:
            col_type = str(self.df[col].dtype)
            columns.append({"name": col, "type": col_type})
        return columns

    def get_file_size(self):
        """Get the size of the opened file."""
        return self.df.memory_usage(deep=True).sum()

    def get_missing_values_count(self):
        """Get the count of missing values in the dataset."""
        return self.df.isnull().sum().sum()

    def get_outliers_count(self):
        """Get the count of outliers in the dataset using Isolation Forest."""
        outliers_count = 0
        for col in self.df.select_dtypes(include=['number']).columns:
            # Преобразуем данные в нужный формат
            data = self.df[col].values.reshape(-1, 1)
            # Обработка пропущенных значений с использованием SimpleImputer
            imputer = SimpleImputer(strategy='mean')
            data = imputer.fit_transform(data)
            # Создаем модель Isolation Forest
            iso_forest = IsolationForest(contamination=0.05)
            # Обучаем модель
            iso_forest.fit(data)
            # Предсказываем выбросы
            outliers = iso_forest.predict(data)
            # Считаем количество выбросов
            outliers_count += (outliers == -1).sum()
        return outliers_count


    def set_analysis_option(self, option, value):
        """Set the analysis option."""
        if option in self.analysis_options:
            self.analysis_options[option] = value

    def set_label_values(self, interface):
        """Set the values for the labels in the interface."""
        file_name_without_extension = os.path.splitext(self.file_name)[0]
        readable_file_size = self.convert_size(self.file_size)
        interface.label_value_file_name.setText(file_name_without_extension)
        interface.label_value_format.setText(self.file_format)
        interface.label_value_sizeFile.setText(readable_file_size)
        interface.label_value_countNull_value.setText(str(self.missing_values_count))
        interface.label_value_outliers_count.setText(str(self.outliers_count))

    def convert_size(self, size_bytes):
        """Convert the file size to a more readable format."""
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    def populate_main_axis_combobox(self, comboBox):
        """Populate the comboBox with suitable columns for the main axis."""
        comboBox.clear()
        for col in self.data_columns:
            if col['type'] in ['int64', 'float64', 'datetime64[ns]']:
                comboBox.addItem(col['name'])

    def populate_list_all_data(self, list_widget, data_columns):
        """Populate the list widget with columns from the dataset."""
        list_widget.clear()
        for col in data_columns:
            item = QListWidgetItem(col['name'])
            list_widget.addItem(item)

    def initialize_logic_manager(self, comboBox, list_all_data, list_changed_data):
        """Initialize LogicManager with comboBox and lists."""
        self.logic_manager.comboBox_main_ox = comboBox
        self.logic_manager.list_all_data = list_all_data
        self.logic_manager.list_changed_data = list_changed_data

        # Populate comboBox_main_ox with suitable columns for the main axis
        self.populate_main_axis_combobox(self.logic_manager.comboBox_main_ox)
        self.logic_manager.comboBox_main_ox.insertItem(0, "Select Main Axis")
        self.logic_manager.comboBox_main_ox.setCurrentIndex(0)

        # Populate list_all_data with columns from the dataset
        self.populate_list_all_data(self.logic_manager.list_all_data, self.data_columns)

        # Connect double-click event to move items between lists
        self.logic_manager.list_all_data.itemDoubleClicked.connect(lambda item: self.logic_manager.move_item_between_lists(item.text(), self.logic_manager.list_all_data, self.logic_manager.list_changed_data))
        self.logic_manager.list_changed_data.itemDoubleClicked.connect(lambda item: self.logic_manager.move_item_between_lists(item.text(), self.logic_manager.list_changed_data, self.logic_manager.list_all_data))

        # Connect comboBox_main_ox change event to update lists and set main axis
        self.logic_manager.comboBox_main_ox.currentIndexChanged.connect(lambda: self.logic_manager.set_main_axis(self.logic_manager.comboBox_main_ox.currentText()))

    def connect_analysis_options(self, interface):
        """Connect checkboxes to analysis options."""
        interface.checkBox_trend_line.stateChanged.connect(lambda state: self.set_analysis_option("trend_line", state == 2))
        interface.checkBox_median.stateChanged.connect(lambda state: self.set_analysis_option("median", state == 2))
        interface.checkBox_average.stateChanged.connect(lambda state: self.set_analysis_option("average", state == 2))
        interface.checkBox_min_max.stateChanged.connect(lambda state: self.set_analysis_option("min_max", state == 2))
        interface.checkBox_moving_average.stateChanged.connect(lambda state: self.set_analysis_option("moving_average", state == 2))
        interface.checkBox_sorting_main_axis.stateChanged.connect(lambda state: self.set_analysis_option("sorting_main_axis", state == 2))
        interface.checkBox_sorting_values_graph.stateChanged.connect(lambda state: self.set_analysis_option("sorting_values_graph", state == 2))
        interface.checkBox_filling_in_blank_values_average.stateChanged.connect(lambda state: self.set_analysis_option("filling_in_blank_values_average", state == 2))
        interface.checkBox_replacing_emissions.stateChanged.connect(lambda state: self.set_analysis_option("replacing_emissions", state == 2))
        interface.checkBox_delete_repetitions.stateChanged.connect(lambda state: self.set_analysis_option("delete_repetitions", state == 2))
        interface.checkBox_decomposition.stateChanged.connect(lambda state: self.set_analysis_option("decomposition", state == 2))

    def create_new_tab(self, tabWidget, tab_name, file_path):
        """Create a new tab with the new interface."""
        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        new_interface = uic.loadUi("UI/new_tab.ui")
        layout.addWidget(new_interface.Frame_main)
        tabWidget.addTab(new_tab, tab_name)
        tabWidget.setCurrentWidget(new_tab)

        # Set label values
        self.set_label_values(new_interface)

        # Initialize LogicManager with comboBox and lists
        self.initialize_logic_manager(new_interface.comboBox_main_ox, new_interface.list_all_data, new_interface.list_changed_data)

        self.connect_analysis_options(new_interface)

        
    def plot_selected_columns(self):
        """Create and display a plot using GraphConstructor."""
        self.main_axis = self.logic_manager.get_main_axis()
        self.selected_data = self.logic_manager.get_selected_data()

        print(f"main axis: {self.main_axis}")
        print(f"selected data: {self.selected_data}")
        print(f"analysis options: {self.analysis_options}")
        print("-----------------------------------")

        graph_constructor = GraphConstructor(self.analysis_options, self.main_axis, self.selected_data)
        graph_constructor.plot_selected_columns(self.df, [self.main_axis], self.selected_data)
