from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

def open_settings_tab(tabWidget):
    """Open a new tab with settings."""
    settings_tab = QWidget()
    layout = QVBoxLayout(settings_tab)
    
    # Add settings widgets here
    layout.addWidget(QLabel("Settings go here"))
    
    tabWidget.addTab(settings_tab, "Settings")
    tabWidget.setCurrentWidget(settings_tab)
