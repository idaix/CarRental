from django.db import models

from agency.models import Agency
from django.urls import reverse
# Create your models here.

# ------------------ VehicleBrand  -----------------
class Make(models.Model):
    name = models.CharField(max_length=100)
    def get_absolute_url(self):
        return reverse('make-change')
    def __str__(self) -> str:
        return self.name

# ------------------ VehicleModel  -----------------
class Model(models.Model):
    make_id = models.ForeignKey(Make, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text='Model')
    series = models.CharField(max_length=100, help_text='Model', blank=True, null=True)
    def get_absolute_url(self):
        return reverse('model-change')
    def __str__(self) -> str:
        return f'{self.make_id.name} {self.name}'
    def get_vehicle_name(self):
        return f'{self.make_id.name} {self.name}'


class Type(models.Model):
    """Represent the type of vehicle"""
    name = models.CharField(max_length=100, help_text='Type of vehicle')
    def get_absolute_url(self):
        return reverse('type-change')
    def __str__(self) -> str:
        return self.name
    

# ------------------ VehicleEngine ----------------------
class Energy(models.Model):
    name = models.CharField(max_length=50, help_text="Engine name")
    def get_absolute_url(self):
        return reverse('energy-change')
    def __str__(self) -> str:
        return self.name

# ------------------ Transmission ----------------------
class Transmission(models.Model):
    name = models.CharField(max_length=20, help_text="Transmission name")
    def get_absolute_url(self):
        return reverse('transmission-change')
    def __str__(self) -> str:
        return self.name

# ------------------ Options ----------------------
# (many to many relation with vehicle model)
class Option(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['name']
    def get_absolute_url(self):
        return reverse('option-change')

# ------------------ Vehicle ----------------------
class Vehicle(models.Model):
    # cumments - Dai Shek
    # A vehicle owned by one & unique Agency(user)
    # price per day example -> (4000.00 DZD, 20000.00 DZD)
    # year example -> (2022) -PositiveSmallIntegerField from 0 to 32767-
    owned_by = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='my_cars')
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='Vehicle price')
    year = models.PositiveSmallIntegerField(help_text="Vehicle year")
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    make = models.ForeignKey(Make, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True)
    engine = models.ForeignKey(Energy, on_delete=models.SET_NULL, null=True)
    transmission = models.ForeignKey(Transmission, on_delete=models.SET_NULL, null=True)
    
    # Thumbnail
    thumbnail = models.OneToOneField('Images', on_delete=models.SET_NULL, null=True, blank=True)

    # Status
    is_available = models.BooleanField(default=True)

    # Details are optional
    color = models.CharField(max_length=50, null=True, blank=True)
    seats = models.PositiveSmallIntegerField(null=True, blank=True)
    doors = models.PositiveSmallIntegerField(null=True, blank=True)
    mileage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=1000, help_text='Small description (1000)', null=True, blank=True)
    # Options
    options = models.ManyToManyField(Option, related_name='vehicle', blank=True)
    # System -----------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    
    # Ordering
    class Meta:
        ordering = ['-created_at']

    # Methods
    def get_title(self):
        if self.model:
            return f'{self.model.get_vehicle_name()} {self.year}'
        else:
            return 'Unknown'
    def get_price(self):
        return f'{self.price} DZD'
    def update_views(self):
        self.views += 1
        return self.views
    def __str__(self) -> str:
        return self.get_title()
    



# ------------------ VehicleImages ------------------
class Images(models.Model):
    # relation with Vehicle [a vehicle can have many images but image belong to one vehicle]
    belong_to = models.ForeignKey(Vehicle, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicle_images/%y/%m/%d', blank=True)
    def __str__(self) -> str:
        return self.belong_to.get_title()


