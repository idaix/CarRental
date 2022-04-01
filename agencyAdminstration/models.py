from distutils.command.upload import upload
from django.db import models

# Create your models here.

# ------------------ VehicleModel Model -----------------
class VehicleModel(models.Model):
    make = models.CharField(max_length=100, help_text='Make')
    model = models.CharField(max_length=100, help_text='Model')
    def __str__(self) -> str:
        return f'{self.make} {self.model}'
    def getModel(self):
        return f'{self.make} {self.model}'

# ------------------ Vehicle Model ----------------------
class Vehicle(models.Model):
    # cumments - Dai Shek
    # price per day example -> (4000.00 DZD, 20000.00 DZD)
    # year example -> (2022) -PositiveSmallIntegerField from 0 to 32767-
     
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='Vehicle price')
    year = models.PositiveSmallIntegerField(help_text="Vehicle year")
    model = models.ForeignKey(VehicleModel, on_delete=models.SET_NULL, null=True)
    
    # Type Choices
    VEHICLES_TYPES = (
        ('c', 'Cars'),
        ('m', 'Motocycles - Scooters'),
        ('tk', 'Truck'),
        ('v', 'Van'),
        ('b', 'Bus'),
        ('bt', 'Boats'),
    )
    vehicle_type = models.CharField(
        max_length=2,
        choices=VEHICLES_TYPES,
        blank=True,
        null=True,
        default='c',
        help_text='Vehicle type',
    )
    
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
        ordering = ['created_at']

    # Methods
    def __str__(self) -> str:
        return self.model.getModel()



# ------------------ VehicleImages Model ------------------
class VehicleImages(models.Model):
    # relation with Vehicle [a vehicle can have many images but image belong to one vehicle]
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/vehicle_images/%y/%m/%d', blank=True)
    def __str__(self) -> str:
        return self.vehicle.color