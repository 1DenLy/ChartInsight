import pyqtgraph as pg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout, QWidget

class GraphConstructor:
    def __init__(self, analysis_options, main_axis, selected_data):
        self.analysis_options = analysis_options
        self.main_axis = main_axis
        self.selected_data = selected_data
        self.current_fig = None

    def create_plot(self, plot_widget, df):
        """Create a plot based on the dataset."""
        plot_widget.clear()
        
        # Convert date columns to datetime
        for col in df.columns:
            if 'date' in col.lower() or 'added' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Determine columns to plot
        x_col = self.main_axis
        y_cols = self.selected_data
        
        if x_col and y_cols:
            for y_col in y_cols:
                plot_widget.plot(df[x_col], df[y_col], pen=pg.mkPen(color='b', width=2), name=y_col)
            plot_widget.setLabel('left', ', '.join(y_cols))
            plot_widget.setLabel('bottom', x_col)
            plot_widget.showGrid(x=True, y=True)
            plot_widget.addLegend()
        else:
            plot_widget.plot([0], [0], pen=pg.mkPen(color='r', width=2), name='No Data')
            plot_widget.setLabel('left', 'No Data')
            plot_widget.setLabel('bottom', 'No Data')
            plot_widget.showGrid(x=True, y=True)
            plot_widget.addLegend()

    def plot_selected_columns(self, df, x_cols, y_cols, tabWidget):
        """Plot the selected columns."""
        if not x_cols or not y_cols:
            print("Please select at least one x-axis and one y-axis column.")
            return

        new_tab = QWidget()
        layout = QVBoxLayout(new_tab)
        fig, ax = plt.subplots()
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        tab_title = f"{', '.join(x_cols)} vs {', '.join(y_cols)}"
        tabWidget.addTab(new_tab, tab_title)
        tabWidget.setCurrentWidget(new_tab)

        for x_col in x_cols:
            if 'date' in x_col.lower() or 'added' in x_col.lower():
                df[x_col] = pd.to_datetime(df[x_col], errors='coerce')
            for y_col in y_cols:
                ax.plot(df[x_col], df[y_col], label=f"{x_col} vs {y_col}")

        ax.set_xlabel(', '.join(x_cols))
        ax.set_ylabel(', '.join(y_cols))
        ax.legend()
        ax.grid(True)
        canvas.draw()

        self.current_fig = fig

    def open_plot_in_window(self):
        """Open the current plot in a separate window."""
        if self.current_fig is not None:
            new_window = plt.figure()
            new_ax = new_window.add_subplot(111)
            for ax in self.current_fig.get_axes():
                for line in ax.get_lines():
                    new_ax.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())
            new_ax.set_xlabel(self.current_fig.get_axes()[0].get_xlabel())
            new_ax.set_ylabel(self.current_fig.get_axes()[0].get_ylabel())
            new_ax.legend()
            new_ax.grid(True)
            plt.close(self.current_fig)  
            plt.show()
