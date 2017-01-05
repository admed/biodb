from django import forms

class SearchFilterForm(forms.Form):

    query = forms.CharField(label=False, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'search phrase','class': 'form-control search-bar'}))
    after_date = forms.DateField(label=False, required=False, widget=forms.DateInput(
        attrs={'placeholder': 'date after', "class": "form-control date-input"}))
    before_date = forms.DateField(label=False, required=False, widget=forms.DateInput(
        attrs={'placeholder': 'date before', "class": "form-control date-input"}))