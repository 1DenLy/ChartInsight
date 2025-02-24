def select_x_axis(self):
        """Select the column for the x-axis."""
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            if item.text() not in [self.listWidget_x_axis.item(i).text() for i in range(self.listWidget_x_axis.count())]:
                self.listWidget_x_axis.addItem(item.text())
            else:
                for i in range(self.listWidget_x_axis.count()):
                    if self.listWidget_x_axis.item(i).text() == item.text():
                        self.listWidget_x_axis.takeItem(i)
                        break

def select_y_axis(self):
    """Select the column for the y-axis."""
    selected_items = self.listWidget.selectedItems()
    for item in selected_items:
        if item.text() not in [self.listWidget_y_axis.item(i).text() for i in range(self.listWidget_y_axis.count())]:
            self.listWidget_y_axis.addItem(item.text())
        else:
            for i in range (self.listWidget_y_axis.count()):
                if self.listWidget_y_axis.item(i).text() == item.text():
                    self.listWidget_y_axis.takeItem(i)
                    break
