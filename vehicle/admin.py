from django.contrib import admin
from .models import Vehicle, Model, Images, Energy, Transmission, Type, Make
# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Make)
admin.site.register(Model)
admin.site.register(Images)
admin.site.register(Energy)
admin.site.register(Type)
admin.site.register(Transmission)