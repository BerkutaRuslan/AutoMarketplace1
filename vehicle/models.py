from colorfield.fields import ColorField
from django.db import models
from Auto_marketplace import settings


class VehicleType(models.Model):
    name = models.CharField(max_length=124)
    photo = models.ImageField(upload_to='vehicletype', default=settings.VEHICLE_DEFAULT_COVER_PATH)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


appointment_choice = (
    ('Road', 'Road'),
    ('Water', 'Water'),
    ('Air', 'Air')
)

condition_choice = (
    ('Factory New', 'Factory New'),
    ('Minimal Wear', 'Minimal Wear'),
    ('Field Tested', 'Field Tested'),
    ('Battle Scarred', 'Battle Scarred')
)


class SingleVehicle(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='vehicles', default=settings.VEHICLE_DEFAULT_COVER_PATH)
    description = models.TextField(max_length=500)
    price = models.IntegerField()
    year = models.DateField()
    horse_power = models.IntegerField()
    engine_cc = models.IntegerField()
    color = ColorField(default='FF0000')
    vehicle_type = models.ForeignKey(VehicleType, related_name='vehicle', on_delete=models.CASCADE)
    vehicle_appointment = models.CharField(choices=appointment_choice, max_length=20, default='Road')
    condition = models.CharField(choices=condition_choice, max_length=40, default='Minimal Wear')
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.name
