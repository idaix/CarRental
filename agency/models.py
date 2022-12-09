from django.db import models
from django.conf import settings
from setup.models import Wilaya, Commune

from PIL import Image


# Subscription
class Subscription(models.Model):
    date_start = models.DateTimeField(auto_now_add=True)
    # date_end = models
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'plan {self.id}'

    def activate(self):
        self.is_active = True
        self.save()
    def deactivate(self):
        self.is_active = False
        self.save()

# create [Profile] model
class Agency(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agency')
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE, related_name='agency', null=True)
    name = models.CharField(max_length=150)
    bio = models.TextField(max_length=500, blank=True, help_text='(500)')
    # image = models.ImageField(default="default/default_profile_image.svg", upload_to='profile_images/%y/%m/%d', blank=True)
    contact_phone = models.CharField(max_length=12, blank=True)
    contact_email = models.CharField(max_length=150, blank=True)
    contact_website = models.CharField(max_length=150, null=True, blank=True)
    # --- no need ---
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    # --- --- ---
    address = models.CharField(max_length=250, blank=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True)
    # --- show on map ---
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)

    available_cars_count = models.IntegerField(default=0)
    
    # system
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    
    def update_views(self):
        self.views += 1
        return self.views
    def __str__(self) -> str:
        return f'{self.name} - {self.user.username}'
    def get_available_cars_count(self):
        allCars = self.my_cars.filter(is_available=True)
        return allCars.count()

    def get_full_address(self):
        return f'{self.wilaya.name}, {self.commune.name} - {self.address}'
    


    def get_geo(self):
        return [float(self.latitude), float(self.longitude)]