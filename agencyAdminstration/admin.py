from django.contrib import admin
from .models import Vehicle, VehicleModel, VehicleImages, VehicleEngine, Transmission, VehicleType, VehicleMake
# Register your models here.
admin.site.register(Vehicle)
admin.site.register(VehicleMake)
admin.site.register(VehicleModel)
admin.site.register(VehicleImages)
admin.site.register(VehicleEngine)
admin.site.register(VehicleType)
admin.site.register(Transmission)