import pyqtgraph as pg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout, QWidget

def create_plot(plot_widget, df):
    """Create a plot based on the dataset."""
    plot_widget.clear()
    
    # Convert date columns to datetime
    for col in df.columns:
        if 'date' in col.lower() or 'added' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Determine columns to plot
    x_col, y_col = determine_plot_columns(df)
    
    if x_col and y_col:
        plot_widget.plot(df[x_col], df[y_col], pen=pg.mkPen(color='b', width=2), name=y_col)
        plot_widget.setLabel('left', y_col)
        plot_widget.setLabel('bottom', x_col)
        plot_widget.showGrid(x=True, y=True)
        plot_widget.addLegend()
    else:
        plot_widget.plot([0], [0], pen=pg.mkPen(color='r', width=2), name='No Data')
        plot_widget.setLabel('left', 'No Data')
        plot_widget.setLabel('bottom', 'No Data')
        plot_widget.showGrid(x=True, y=True)
        plot_widget.addLegend()

def determine_plot_columns(df):
    """Determine the best columns to plot."""
    numeric_cols = df.select_dtypes(include=['number']).columns
    date_cols = df.select_dtypes(include=['datetime']).columns
    
    if not numeric_cols.empty and not date_cols.empty:
        return date_cols[0], numeric_cols[0]
    elif not numeric_cols.empty:
        return df.columns[0], numeric_cols[0]
    else:
        return None, None

def plot_selected_columns(df, x_cols, y_cols, tabWidget):
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

    return fig

def open_plot_in_window(current_fig):
    """Open the current plot in a separate window."""
    if current_fig is not None:
        new_window = plt.figure()
        new_ax = new_window.add_subplot(111)
        for ax in current_fig.get_axes():
            for line in ax.get_lines():
                new_ax.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())
        new_ax.set_xlabel(current_fig.get_axes()[0].get_xlabel())
        new_ax.set_ylabel(current_fig.get_axes()[0].get_ylabel())
        new_ax.legend()
        new_ax.grid(True)
        plt.close(current_fig)  
        plt.show()
