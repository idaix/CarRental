from django.contrib import admin
from .models import Vehicle, VehicleModel, VehicleImages
# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleModel)
admin.site.register(VehicleImages)