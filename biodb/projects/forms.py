from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import RObject

class SearchFilterForm(forms.Form):

    query = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'search phrase','class': 'form-control search-bar'}))
    after_date = forms.DateField(label=False, required=False, widget=forms. DateInput(
        attrs={'placeholder': 'date after', "class": "form-control date-input"})) # FIXME: Find how to make this input 'number only' like in line_bank
    before_date = forms.DateField(label=False, required=False, widget=forms. DateInput(
        attrs={'placeholder': 'date before', "class": "form-control date-input"}))

class RObjectCreateForm(forms.ModelForm):
    """
    Forms for creating Robject Instance
    """
    required_css_class = 'required'
    notes = forms.CharField(
        widget=CKEditorWidget(), required=False)
    
    
    class Meta:
        model = RObject
        fields = '__all__'
        exclude = ['created_by', 'project', 'bio_obj', 'changed_by']
        # fields = ('name', 'organism', 'tissue', 'cell_type', 'product_format', 'culture_properties', 'biosafety_level', 'disease', 'age', 'gender',
        #           'ethnicity', 'storage_conditions', 'derivation', 'clinical_data', 'comments', 'subculturing',
        #           'cryopreservation', 'culture_conditions', 'rack', 'box', 'entry', 'complete_growth_medium')