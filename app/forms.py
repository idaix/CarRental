from django.forms import ModelForm

from order.models import Client, Order

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'mobile', 'email', 'gender', 'age', 'purpose']