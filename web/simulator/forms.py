from .models import Experiment, TimeStep
from django import forms


class ExperimentForm(forms.ModelForm):
    '''A form based off the  Experiment model.'''
    class Meta:
        model = Experiment
        exclude = [
            'init_report',
            'final_summary',
        ]
