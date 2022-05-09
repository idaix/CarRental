from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from agency.models import Agency


class UserForm(ModelForm):
    class Meta:
        model=get_user_model()
        fields = '__all__'
class AgencyForm(ModelForm):
    class Meta:
        model=Agency
        fields = '__all__'
