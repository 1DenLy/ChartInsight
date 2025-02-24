from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton
import os

class WindowManager:
    def __init__(self, window):
        self.window = window

    def save_window_settings(self):
        """Save window size, position, and splitter state on close using QSettings."""
        settings = QSettings("YourCompany", "YourApp")
        settings.setValue("size", self.window.size())
        settings.setValue("position", self.window.pos())
        settings.setValue("splitterState", self.window.splitter.saveState())

    def load_window_settings(self):
        """Load window size, position, and splitter state using QSettings."""
        settings = QSettings("YourCompany", "YourApp")
        size = settings.value("size")
        position = settings.value("position")
        splitter_state = settings.value("splitterState")
        if size:
            self.window.resize(size)
        if position:
            self.window.move(position)
        if splitter_state:
            self.window.splitter.restoreState(splitter_state)

    def close_tab(self, index):
        """Close the tab by index."""
        if self.window.tabWidget.tabText(index) != "Home":
            self.window.tabWidget.removeTab(index)

    def resize_window(self, event):
        """Handle window resize event."""
        super(self.window.__class__, self.window).resizeEvent(event)
        
        # Get new window dimensions
        new_width = self.window.width()
        new_height = self.window.height()

        # Scale the central widget proportionally to the window size
        self.window.window.setFixedSize(new_width, new_height)

    def load_and_set_icons(self):
        """Load and set icons on labels based on button names."""
        icon_folder = os.path.join('resources', 'icons')
        for button in self.window.findChildren(QPushButton):
            icon_name = f"{button.objectName()}.png"
            icon_path = os.path.join(icon_folder, icon_name)
            if os.path.exists(icon_path):
                label_name = f"icon_{button.objectName()}"
                label = self.window.findChild(QLabel, label_name)
                if label:
                    pixmap = QPixmap(icon_path)
                    resized_pixmap = pixmap.scaledToHeight(button.height())
                    label.setPixmap(resized_pixmap)
