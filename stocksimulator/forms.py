from pyexpat import model
from django import forms
from .models import Csv

class CsvForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ('csv_file',)
        