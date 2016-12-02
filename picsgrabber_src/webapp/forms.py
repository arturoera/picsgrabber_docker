from django import forms
from .models import Grabber


class GrabberForm(forms.ModelForm):
    class Meta:
        model = Grabber
        fields = ('image_id', 'description', 'url')
