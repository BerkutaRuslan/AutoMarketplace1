from django.contrib import admin

# Register your models here.
from vehicle.models import SingleVehicle, VehicleType


class AdminVehicleType(admin.ModelAdmin):
    list_display = ('name', 'description')


class AdminSingleVehicle(admin.ModelAdmin):
    list_display = ('name', 'price', 'year', 'horse_power', 'color',
                    'land_vehicle', 'water_vehicle', 'air_vehicle')


admin.site.register(VehicleType, AdminVehicleType)
admin.site.register(SingleVehicle, AdminSingleVehicle)
