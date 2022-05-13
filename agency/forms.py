from vehicle.models import Vehicle
from .models import Agency
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from accounts.models import User


# PROFILE FORMS
class RegisterUserForm(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields = ['username', 'email', 'password1', 'password2']
class RegisterAgencyForm(ModelForm):
    class Meta:
        model=Agency
        fields = ['name', 'contact_phone', 'contact_email', 'contact_website']

class UserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['image', 'username', 'email',]

class ProfileForm(ModelForm):
    class Meta:
        model=Agency
        fields = ['name', 'bio','contact_phone', 'contact_email', 'contact_website', 'address']

# VEHCILE FORMS
class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ['year', 'type', 'price','engine', 'transmission', 'color', 'seats', 'doors', 'options', 'description'] 
