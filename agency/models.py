from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# SIGNALS...
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# [Location] model
class Location(models.Model):
    user = models.ForeignKey('Agency', related_name='location', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    lon = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self) -> str:
        return self.name


# create [Profile] model
class Agency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    bio = models.TextField(max_length=500, blank=True, help_text='(500)')
    image = models.ImageField(default="default/default_profile_image.svg", upload_to='profile_images/%y/%m/%d', blank=True)
    contact_phone = models.CharField(max_length=12, blank=True)
    contact_email = models.CharField(max_length=150, blank=True)
    contact_website = models.CharField(max_length=150, null=True, blank=True)

    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.user.username}'


# -----------------------------------------
# how it work? 
# - Signup [create user]
#   - signal
#   - call function -> create_user_profile
#   - create the profile for this user ...
# -----------------------------------------
# @receiver(post_save, sender=User) #connect this function with the user [the user sends a signal, reciever took the signal & call the function...]
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Agency.objects.create(
#             user=instance
#         )