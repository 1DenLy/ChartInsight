# ChartInsight

ChartInsight is a data analysis and visualization tool built using PyQt5 and Matplotlib. It allows users to load data from various file formats, validate the data, and create interactive plots.

## Features

- Load data from CSV, Excel, and JSON files.
- Validate data for analysis.
- Select columns for the x-axis and y-axis.
- Create interactive plots.
- Open plots in a separate window.
- Save and load window settings.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/1DenLy/ChartInsight.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ChartInsight
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```bash
    python main.py
    ```

2. Use the UI to load data, select columns, and create plots.

## Project Structure

```
ChartInsight/
├── main.py
├── modules/
│   ├── data_loader.py
│   ├── data_validator.py
│   ├── data_visualizer.py
│   ├── window_manager.py
├── UI/
│   ├── main_window.ui
├── window_settings.json
├── requirements.txt
```

### main.py

The main entry point of the application. It initializes the UI and connects the buttons to their respective functions.

### modules/data_loader.py

Contains functions to load data from files and populate the list view with column names.

### modules/data_validator.py

Contains functions to validate the data for analysis.

### modules/data_visualizer.py

Contains functions to create plots and open plots in a separate window.

### modules/window_manager.py

Contains functions to save and load window settings, handle window resize events, and close tabs.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.