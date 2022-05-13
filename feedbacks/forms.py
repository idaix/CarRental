

from dataclasses import field
from .models import feedback
from django import forms


class FeedbackForm(forms.ModelForm):
    class Meta:
        model=feedback
        fields=['comment']

