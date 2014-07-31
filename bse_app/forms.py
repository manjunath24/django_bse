from django import forms

from bse_app.models import Company


class GraphForm(forms.Form):
    company_name = forms.ModelChoiceField(queryset=Company.objects.all())
    start_date = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y'))
    end_date = forms.DateField(widget=forms.DateInput(format='%m/%d/%Y'))