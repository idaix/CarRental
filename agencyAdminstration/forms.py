from django.forms import ModelForm, ModelChoiceField
from .models import Vehicle

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ['model', 'year', 'type', 'price','engine', 'transmission', 'color', 'seats', 'doors', 'mileage', 'description'] 

    # args -> request.POST, kwargs -> owned_by
    # def __init__(self, *args, **kwargs):
    #     owned_by = kwargs.pop('owned_by', '')
    #     super(AddVehicleForm, self).__init__(*args, **kwargs)
    #     self.fields['owned_by']=ModelChoiceField(queryset=Vehicle.objects.filter(owned_by=owned_by))
