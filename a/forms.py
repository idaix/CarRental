from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from agency.models import Agency


class UserForm(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields = '__all__'

class AdminForm(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

class AgencyForm(ModelForm):
    class Meta:
        model=Agency
        fields = '__all__'

class AgencyFormCreate(ModelForm):
    class Meta:
        model=Agency
        fields = ['name', 'contact_phone', 'contact_email', 'contact_website']
