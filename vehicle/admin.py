from django.contrib import admin

# Register your models here.
from vehicle.models import SingleVehicle, VehicleType

admin.site.register(VehicleType)
admin.site.register(SingleVehicle)
