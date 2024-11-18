from django import forms
from .models import RecyclingActivity

class RecyclingActivityForm(forms.ModelForm):
    class Meta:
        model = RecyclingActivity
        fields = ['plastic', 'paper', 'glass', 'metal']