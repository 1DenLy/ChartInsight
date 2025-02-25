import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

def calculate_trend_line(df, x_col, y_col):
    """Calculate the trend line for the given columns."""
    # Преобразуем столбец x_col в числовой формат, если он является датой
    if np.issubdtype(df[x_col].dtype, np.datetime64):
        df[x_col] = df[x_col].astype(np.int64) // 10**9  # Преобразуем в секунды с начала эпохи

    z = np.polyfit(df[x_col], df[y_col], 1)
    p = np.poly1d(z)
    return p(df[x_col])

def calculate_median(df, y_col):
    """Calculate the median for the given column."""
    return df[y_col].median()

def calculate_average(df, y_col):
    """Calculate the average for the given column."""
    return df[y_col].mean()

def calculate_min_max(df, y_col):
    """Calculate the minimum and maximum for the given column."""
    return df[y_col].min(), df[y_col].max()

def sort_main_axis(df, main_axis):
    """Sort the dataframe by the main axis."""
    return df.sort_values(by=main_axis)

def replace_emissions(df, contamination=0.05):
    """Replace emissions (outliers) in the dataset using Isolation Forest."""
    for col in df.select_dtypes(include=['number']).columns:
        data = df[col].values.reshape(-1, 1)
        imputer = SimpleImputer(strategy='mean')
        data = imputer.fit_transform(data)
        iso_forest = IsolationForest(contamination=contamination)
        iso_forest.fit(data)
        outliers = iso_forest.predict(data)
        df.loc[outliers == -1, col] = np.nan  # Replace outliers with NaN
        df[col] = imputer.fit_transform(df[col].values.reshape(-1, 1))  # Fill NaN with mean
    return df

def calculate_moving_average(df, y_col, window=5):
    """Calculate the moving average for the given column."""
    return df[y_col].rolling(window=window).mean()

def delete_repetitions(df):
    """Delete repeated rows in the dataset."""
    return df.drop_duplicates()

def decompose_series(df, y_col, model='additive', period=12):
    """Decompose the time series data to smooth the values."""
    result = seasonal_decompose(df[y_col], model=model, period=period)
    return result.trend

def smooth_series(df, y_col, window=12):
    """Smooth the series using a simple moving average."""
    return df[y_col].rolling(window=window).mean()
