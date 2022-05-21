import email
from pyexpat import model
from django.db import models

# Create your models here.

class HelpMessage(models.Model):
    email = models.CharField(max_length=150)
    message = models.TextField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering=['-date_added']

    def __str__(self) -> str:
        return self.email