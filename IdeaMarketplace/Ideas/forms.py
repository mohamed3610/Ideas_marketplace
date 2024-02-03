from django import forms
from django import forms
from .models import Score
from django.core.exceptions import ValidationError



class AddTagsForm(forms.Form):
    tags = forms.CharField(max_length=255)



class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['feasibility', 'market_value', 'cost_effective', 'risk', 'originality', 'value_proposition']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize the form fields here if needed

    def clean(self):
        cleaned_data = super().clean()
        # Additional validation logic can be added here if needed

        # Example: Ensure that the sum of scores is within a certain range



        return cleaned_data
