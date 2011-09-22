from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _

from common.helpers import uniqify


class EnhancedForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    
                    
class EnhancedModelForm(forms.ModelForm):
    error_css_class = EnhancedForm.error_css_class
    required_css_class = EnhancedForm.required_css_class
    
    def __init__(self, *args, **kwargs):
        super(EnhancedModelForm, self).__init__(*args, **kwargs)
        
        # when subclassing a subclassed form with extra fields
        # remove those fields when the field is in exclude list
        for field_name in getattr(self.Meta, 'exclude', ()):
            if self.fields.has_key(field_name):
                del self.fields[field_name]
        
        # create combined_fields
        self.combined_fields = getattr(self.Meta, 'combined_fields', ())
        for combinations in self.combined_fields:
            _label_set = []
            _error_set = []
            _css_classes_set = []
            _first_field = None
            for counter, field_name in enumerate(combinations):
                field = self.fields[field_name]

                _label_set.append(field.label.lower())
                _error_set += self.errors.get(field_name, [])
                _css_classes_set.append(self[field_name].css_classes())
                field.combined = { 'first': False, 'last': False }
                if counter == 0:
                    _first_field = field
                    field.combined['first'] = True
                elif counter == len(combinations) - 1:
                    field.combined['last'] = True
            
            _first_field.combined['label'] = ' + '.join(_label_set)
            _first_field.combined['label'] = _first_field.combined['label'].capitalize()
            _first_field.combined['errors'] = ErrorList(uniqify(_error_set, True))
            _first_field.combined['css_classes'] = ' '.join(_css_classes_set)
