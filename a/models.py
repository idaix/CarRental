import email
from pyexpat import model
from django.db import models
from datetime import datetime

# Create your models here.

class HelpMessage(models.Model):
    email = models.CharField(max_length=150)
    message = models.TextField(max_length=1000)
    reply = models.TextField(max_length=1000, blank=True, null=True)

    is_replied = models.BooleanField(default=False)

    date_added = models.DateTimeField(auto_now_add=True, null=True)
    reply_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering=['-date_added']

    def update_date(self):
        self.reply_date = datetime.now()
    def __str__(self) -> str:
        return self.email