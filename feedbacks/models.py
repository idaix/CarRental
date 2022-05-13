
# Create your models here.
from django.db import models
from agency.models import *
from django.contrib.auth.models import User
# Create your models here.
class feedback(models.Model):
    client=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    agency=models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='agency')
    comment=models.CharField(max_length=150,null=True,blank=True)

def __str__(self) -> str:
    return f'{self.client} to {self.agency}' 