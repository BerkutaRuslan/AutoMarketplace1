# Generated by Django 3.0.6 on 2020-09-23 10:17

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=124)),
                ('photo', models.ImageField(default='vehicle_type/default.png', upload_to='media/vehicletype')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SingleVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('photo', models.ImageField(default='vehicle/default.png', upload_to='media/vehicles')),
                ('description', models.TextField(max_length=500)),
                ('price', models.IntegerField()),
                ('year', models.DateField()),
                ('horse_power', models.IntegerField()),
                ('engine_cc', models.IntegerField()),
                ('color', colorfield.fields.ColorField(default='FF0000', max_length=18)),
                ('vehicle_appointment', models.CharField(choices=[('Road', 'Road'), ('Water', 'Water'), ('Air', 'Air')], default='Road', max_length=20)),
                ('condition', models.CharField(choices=[('FactoryNew', 'FactoryNew'), ('Minimal Wear', 'Minimal Wear'), ('Field Tested', 'Field Tested'), ('Battle Scarred', 'Battle Scarred')], default='Minimal Wear', max_length=40)),
                ('is_new', models.BooleanField(default=False)),
                ('vehicle_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle', to='vehicle.VehicleType')),
            ],
        ),
    ]
