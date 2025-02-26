import pyqtgraph as pg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
from modules.data_analysis import calculate_trend_line, calculate_median, calculate_average, calculate_min_max, sort_main_axis, replace_emissions, calculate_moving_average, delete_repetitions, decompose_series, smooth_series

class GraphConstructor:
    def __init__(self, analysis_options, main_axis, selected_data):
        self.analysis_options = analysis_options
        self.main_axis = main_axis
        self.selected_data = selected_data
        self.current_fig = None

    def plot_selected_columns(self, df, x_cols, y_cols):
        """Plot the selected columns in a new window."""
        
        print(x_cols, y_cols)

        if not x_cols or not y_cols:
            print("Please select at least one x-axis and one y-axis column.")
            return

        # Создаем копию DataFrame, чтобы не изменять оригинальные данные
        df_copy = df.copy()

        fig, ax = plt.subplots()

        if self.analysis_options.get("replacing_emissions"):
            df_copy = replace_emissions(df_copy)

        if self.analysis_options.get("sorting_main_axis"):
            df_copy = sort_main_axis(df_copy, self.main_axis)

        if self.analysis_options.get("delete_repetitions"):
            df_copy = delete_repetitions(df_copy)

        def get_random_color():
            """Generate a random color."""
            return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])

        for x_col in x_cols:
            if 'date' in x_col.lower() or 'added' in x_col.lower():
                df_copy[x_col] = pd.to_datetime(df_copy[x_col], errors='coerce')
                df_copy = df_copy.dropna(subset=[x_col])  # Удаляем строки с некорректными датами
                df_copy[x_col] = df_copy[x_col].astype(np.int64) // 10**9  # Преобразуем в секунды с начала эпохи

            for y_col in y_cols:
                ax.plot(df_copy[x_col], df_copy[y_col], label=f"{x_col} vs {y_col}")

                if self.analysis_options.get("trend_line"):
                    trend_line = calculate_trend_line(df_copy, x_col, y_col)
                    ax.plot(df_copy[x_col], trend_line, label=f"Trend Line ({y_col})", linestyle='--', color=get_random_color())

                if self.analysis_options.get("median"):
                    median = calculate_median(df_copy, y_col)
                    ax.axhline(median, color=get_random_color(), linestyle='--', label=f"Median ({y_col})")

                if self.analysis_options.get("average"):
                    average = calculate_average(df_copy, y_col)
                    ax.axhline(average, color=get_random_color(), linestyle='--', label=f"Average ({y_col})")

                if self.analysis_options.get("min_max"):
                    min_val, max_val = calculate_min_max(df_copy, y_col)
                    ax.axhline(min_val, color=get_random_color(), linestyle='--', label=f"Min ({y_col})")
                    ax.axhline(max_val, color=get_random_color(), linestyle='--', label=f"Max ({y_col})")

                if self.analysis_options.get("moving_average"):
                    moving_average = calculate_moving_average(df_copy, y_col)
                    ax.plot(df_copy[x_col], moving_average, label=f"Moving Average ({y_col})", linestyle='--', color=get_random_color())

                #if self.analysis_options.get("decomposition"):
                    #decomposed = decompose_series(df_copy, y_col)
                    #ax.plot(df_copy[x_col], decomposed, label=f"Decomposed ({y_col})", linestyle='--', color=get_random_color())

                if self.analysis_options.get("decomposition"):
                    smoothed = smooth_series(df_copy, y_col)
                    ax.plot(df_copy[x_col], smoothed, label=f"Smoothed ({y_col})", linestyle='--', color=get_random_color())

        ax.set_xlabel(', '.join(x_cols))
        ax.set_ylabel(', '.join(y_cols))
        ax.legend()
        ax.grid(True)
        plt.show()
        return fig  # Return the plot figure

