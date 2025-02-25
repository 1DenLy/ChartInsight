from PyQt5.QtWidgets import QListWidget

# Step 1: Define the class and initialize necessary attributes
class LogicManager:
    def __init__(self):
        self.main_axis = None  # Current selected main axis
        self.data = None  # Main dataset
        self.list_all_data = QListWidget()  # List for all data
        self.list_changed_data = QListWidget()  # List for changed data

    # Step 2: Method to load data
    def load_data(self, file_path):
        """Load data from the file."""
        # Logic to load data from the file
        pass

    # Step 3: Method to set the main axis
    def set_main_axis(self, axis):
        """Set the main axis."""
        # Return the previous main axis to the list_all_data if it was set
        if self.main_axis and self.main_axis != "Select Main Axis":
            self.return_main_axis_to_list(self.main_axis)
            
            self.sort_list(self.list_all_data)
            self.sort_list(self.list_changed_data)

        self.main_axis = axis
        self.update_lists()

    def return_main_axis_to_list(self, axis):
        """Return the previous main axis to the list_all_data."""
        if axis not in [self.list_all_data.item(i).text() for i in range(self.list_all_data.count())]:
            self.list_all_data.addItem(axis)

    # Step 4: Method to add selected data
    def add_selected_data(self, data):
        """Add selected data to the changed data list."""
        if data not in [self.list_changed_data.item(i).text() for i in range(self.list_changed_data.count())]:
            self.list_changed_data.addItem(data)
            for i in range(self.list_all_data.count()):
                if self.list_all_data.item(i).text() == data:
                    self.list_all_data.takeItem(i)
                    break

    # Step 5: Method to remove selected data
    def remove_selected_data(self, data):
        """Remove selected data from the changed data list."""
        for i in range(self.list_changed_data.count()):
            if self.list_changed_data.item(i).text() == data:
                self.list_changed_data.takeItem(i)
                break
        if data not in [self.list_all_data.item(i).text() for i in range(self.list_all_data.count())]:
            self.list_all_data.addItem(data)

    # Step 6: Method to ensure unique items across lists
    def ensure_unique_items(self):
        """Ensure items are unique across both lists."""
        all_items = set()
        for i in range(self.list_all_data.count()):
            item = self.list_all_data.item(i)
            if item:
                all_items.add(item.text())

        for i in range(self.list_changed_data.count()):
            item = self.list_changed_data.item(i)
            if item:
                if item.text() in all_items:
                    self.list_changed_data.takeItem(i)
                    i -= 1
                else:
                    all_items.add(item.text())

    # Step 7: Method to update lists based on the main axis
    def update_lists(self):
        """Update the lists to exclude the selected main axis."""
        if self.main_axis:
            for i in range(self.list_all_data.count()):
                item = self.list_all_data.item(i)
                if item and item.text() == self.main_axis:
                    self.list_all_data.takeItem(i)
                    i -= 1

            for i in range(self.list_changed_data.count()):
                item = self.list_changed_data.item(i)
                if item and item.text() == self.main_axis:
                    self.list_changed_data.takeItem(i)
                    i -= 1

    # Step 8: Method to handle double-click event to move items between lists
    def move_item_between_lists(self, item_text, source_list, target_list):
        """Move item between lists."""
        for i in range(source_list.count()):
            item = source_list.item(i)
            if item and item.text() == item_text:
                source_list.takeItem(i)
                target_list.addItem(item_text)
                break
        self.sort_list(source_list)
        self.sort_list(target_list)

    def sort_list(self, list_widget):
        """Sort the items in the list widget."""
        items = [list_widget.item(i).text() for i in range(list_widget.count())]
        items.sort()
        list_widget.clear()
        for item in items:
            list_widget.addItem(item)

    def get_main_axis(self):
        """Get the current main axis."""
        return self.main_axis

    def get_selected_data(self):
        """Get the selected data."""
        return [self.list_changed_data.item(i).text() for i in range(self.list_changed_data.count())]
