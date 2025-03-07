from django.forms.widgets import FileInput
from django.utils.translation import gettext_lazy as _

class MultipleFileInput(FileInput):
    allow_multiple_selected = True
    template_name = 'products/custom_widget_templates/custom_widget_templates/multiple_file_input.html'

    def __init__(self, attrs=None):
        default_attrs = {'multiple': True}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        return files.getlist(name)