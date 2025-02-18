import json

def save_window_settings(window):
    """Save window size and position on close."""
    settings = {
        'size': (window.size().width(), window.size().height()),
        'position': (window.pos().x(), window.pos().y())
    }
    with open('window_settings.json', 'w') as f:
        json.dump(settings, f)

def load_window_settings(window):
    """Load window size and position."""
    try:
        with open('window_settings.json', 'r') as f:
            settings = json.load(f)
            window.resize(settings['size'][0], settings['size'][1])
            window.move(settings['position'][0], settings['position'][1])
    except (FileNotFoundError, json.JSONDecodeError):
        pass

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
