from django_filters.widgets import RangeWidget
from django.contrib.admin.widgets import AdminDateWidget

class RangePickerWidget(RangeWidget):
    def __init__(self, attrs=None):
        widgets = (AdminDateWidget(format='%Y-%m-%d'), AdminDateWidget(format='%Y-%m-%d'))
        super(RangeWidget, self).__init__(widgets, attrs)
        