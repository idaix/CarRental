from .models import feedback
from django.forms import ModelForm


class FeedbackForm(ModelForm):
    class Meta:
        model=feedback
        fields=['comment']
