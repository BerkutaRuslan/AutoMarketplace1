from django.contrib import admin

# Register your models here.
from vehicle.models import SingleVehicle, VehicleType


class AdminVehicleType(admin.ModelAdmin):
    list_display = ('name', 'description')


class AdminSingleVehicle(admin.ModelAdmin):
    list_display = ('name', 'price', 'year', 'horse_power', 'color', 'engine_cc',
                    'vehicle_appointment', 'condition', 'is_new')


admin.site.register(VehicleType, AdminVehicleType)
admin.site.register(SingleVehicle, AdminSingleVehicle)
