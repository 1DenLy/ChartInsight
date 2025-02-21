from PyQt5.QtCore import QSettings

def save_window_settings(window):
    """Save window size and position on close using QSettings."""
    settings = QSettings("YourCompany", "YourApp")
    settings.setValue("size", window.size())
    settings.setValue("position", window.pos())

def load_window_settings(window):
    """Load window size and position using QSettings."""
    settings = QSettings("YourCompany", "YourApp")
    size = settings.value("size")
    position = settings.value("position")
    if size:
        window.resize(size)
    if position:
        window.move(position)

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
