from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_agent = models.BooleanField(default=False)
    image = models.ImageField(default="default/default_profile_image.svg", upload_to='profile_images/%y/%m/%d', blank=True)
    def __str__(self):
        return self.username