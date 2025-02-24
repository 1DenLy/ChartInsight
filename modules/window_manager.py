from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton
import os

def save_window_settings(window):
    """Save window size, position, and splitter state on close using QSettings."""
    settings = QSettings("YourCompany", "YourApp")
    settings.setValue("size", window.size())
    settings.setValue("position", window.pos())
    settings.setValue("splitterState", window.splitter.saveState())

def load_window_settings(window):
    """Load window size, position, and splitter state using QSettings."""
    settings = QSettings("YourCompany", "YourApp")
    size = settings.value("size")
    position = settings.value("position")
    splitter_state = settings.value("splitterState")
    if size:
        window.resize(size)
    if position:
        window.move(position)
    if splitter_state:
        window.splitter.restoreState(splitter_state)

def close_tab(window, index):
    """Close the tab by index."""
    if window.tabWidget.tabText(index) != "Home":
        window.tabWidget.removeTab(index)

def resize_window(window, event):
    """Handle window resize event."""
    super(window.__class__, window).resizeEvent(event)
    
    # Get new window dimensions
    new_width = window.width()
    new_height = window.height()

    # Scale the central widget proportionally to the window size
    window.window.setFixedSize(new_width, new_height)

def load_and_set_icons(window):
    """Load and set icons on labels based on button names."""
    icon_folder = os.path.join('resources', 'icons')
    for button in window.findChildren(QPushButton):
        icon_name = f"{button.objectName()}.png"
        icon_path = os.path.join(icon_folder, icon_name)
        if os.path.exists(icon_path):
            label_name = f"icon_{button.objectName()}"
            label = window.findChild(QLabel, label_name)
            if label:
                pixmap = QPixmap(icon_path)
                resized_pixmap = pixmap.scaledToHeight(button.height())
                label.setPixmap(resized_pixmap)
