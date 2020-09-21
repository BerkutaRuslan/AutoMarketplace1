from colorfield.fields import ColorField
from django.db import models
from Auto_marketplace import settings
from Auto_marketplace.utils import get_file_path


class VehicleType(models.Model):
    name = models.CharField(max_length=124)
    photo = models.FileField(upload_to=get_file_path, default=settings.VEHICLE_TYPE_DEFAULT_COVER_PATH)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class SingleVehicle(models.Model):
    name = models.CharField(max_length=50)
    photo = models.FileField(upload_to=get_file_path, default=settings.VEHICLE_DEFAULT_COVER_PATH)
    description = models.TextField(max_length=500)
    price = models.FloatField()
    year = models.DateField()
    horse_power = models.IntegerField()
    engine_cc = models.IntegerField()
    color = ColorField(default='FF0000')
    vehicle_type = models.ForeignKey(VehicleType, related_name='vehicle', on_delete=models.CASCADE)
    land_vehicle = models.BooleanField(default=True)
    water_vehicle = models.BooleanField(default=False)
    air_vehicle = models.BooleanField(default=False)

    def __str__(self):
        return self.name
