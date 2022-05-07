from django.db import models
from django.conf import settings
from setup.models import Wilaya, Commune

from PIL import Image

# create [Profile] model
class Agency(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agency')
    name = models.CharField(max_length=150)
    bio = models.TextField(max_length=500, blank=True, help_text='(500)')
    image = models.ImageField(default="default/default_profile_image.svg", upload_to='profile_images/%y/%m/%d', blank=True)
    contact_phone = models.CharField(max_length=12, blank=True)
    contact_email = models.CharField(max_length=150, blank=True)
    contact_website = models.CharField(max_length=150, null=True, blank=True)

    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=250, blank=True)

    wilaya = models.ForeignKey(Wilaya, on_delete=models.SET_NULL, null=True)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL, null=True)
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