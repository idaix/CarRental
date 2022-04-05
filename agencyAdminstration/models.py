from django.db import models

# Import user model to use_it as Agency Model
from django.contrib.auth.models import User

# Create your models here.

# ------------------ VehicleModel  -----------------
class VehicleModel(models.Model):
    make = models.CharField(max_length=100, help_text='Make')
    model = models.CharField(max_length=100, help_text='Model')
    def __str__(self) -> str:
        return f'{self.make} {self.model}'
    def getModel(self):
        return f'{self.make} {self.model}'


class VehicleType(models.Model):
    """Represent the type of vehicle"""
    name = models.CharField(max_length=100, help_text='Type of vehicle')
    def __str__(self) -> str:
        return self.name

# ------------------ VehicleEngine ----------------------
class VehicleEngine(models.Model):
    name = models.CharField(max_length=50, help_text="Engine name")
    def __str__(self) -> str:
        return self.name

# ------------------ Transmission ----------------------
class Transmission(models.Model):
    name = models.CharField(max_length=20, help_text="Transmission name")
    def __str__(self) -> str:
        return self.name

# ------------------ Vehicle ----------------------
class Vehicle(models.Model):
    # cumments - Dai Shek
    # A vehicle owned by one & unique Agency(user)
    # price per day example -> (4000.00 DZD, 20000.00 DZD)
    # year example -> (2022) -PositiveSmallIntegerField from 0 to 32767-
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='Vehicle price')
    year = models.PositiveSmallIntegerField(help_text="Vehicle year")
    type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True)
    engine = models.ForeignKey(VehicleEngine, on_delete=models.SET_NULL, null=True)
    transmission = models.ForeignKey(Transmission, on_delete=models.SET_NULL, null=True)
    
    # Thumbnail
    thumbnail = models.OneToOneField('VehicleImages', on_delete=models.SET_NULL, null=True, blank=True)


    # # Type Choices
    # VEHICLES_TYPES = (
    #     ('c', 'Cars'),
    #     ('m', 'Motocycles - Scooters'),
    #     ('tk', 'Truck'),
    #     ('v', 'Van'),
    #     ('b', 'Bus'),
    #     ('bt', 'Boats'),
    # )
    # vehicle_type = models.CharField(
    #     max_length=2,
    #     choices=VEHICLES_TYPES,
    #     blank=True,
    #     null=True,
    #     default='c',
    #     help_text='Vehicle type',
    # )
    
    # Status
    is_available = models.BooleanField(default=True)

    # Details are optional
    color = models.CharField(max_length=50, null=True, blank=True)
    seats = models.PositiveSmallIntegerField(null=True, blank=True)
    doors = models.PositiveSmallIntegerField(null=True, blank=True)
    mileage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=1000, help_text='Small description (1000)')
    
    # System -----------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Ordering
    class Meta:
        ordering = ['-created_at']

    # Methods
    def __str__(self) -> str:
        return f'{self.model.getModel()} {self.year} by {self.owned_by}'



# ------------------ VehicleImages ------------------
class VehicleImages(models.Model):
    # relation with Vehicle [a vehicle can have many images but image belong to one vehicle]
    belong_to = models.ForeignKey(Vehicle, related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vehicle_images/%y/%m/%d', blank=True)
    def __str__(self) -> str:
        return self.belong_to.model.getModel()