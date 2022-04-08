from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
# [Location] model
class Location(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name


# create [Profile] model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    image = models.ImageField(default="default_profile_image.jpg", upload_to='profile_images/%y/%m/%d', blank=True)
    contact_phone = models.CharField(max_length=12)
    contact_website = models.CharField(max_length=150, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)


    def __str__(self) -> str:
        return f'{self.name} - {self.user.username}'

    # def save(self):
    #     super().save()
    #     if self.image:
    #         thumbnail = Image.open(self.image.path)
    #         if thumbnail.height > 300 or thumbnail.width > 300:
    #             output_size = (300, 300)
    #             thumbnail.thumbnail(output_size)
    #             thumbnail.save(self.image.path)



# -----------------------------------------
# how it work? 
# - Signup [create user]
#   - signal
#   - call function -> create_user_profile
#   - create the profile for this user ...
# -----------------------------------------
@receiver(post_save, sender=User) #connect this function with the user [the user sends a signal, reciever took the signal & call the function...]
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )