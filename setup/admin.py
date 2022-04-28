from django.contrib import admin

# Register your models here.
from .models import Wilaya, Commune

admin.site.register(Wilaya)
admin.site.register(Commune)