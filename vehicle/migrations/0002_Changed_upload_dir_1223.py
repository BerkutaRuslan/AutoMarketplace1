# Generated by Django 3.0.6 on 2020-09-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlevehicle',
            name='photo',
            field=models.ImageField(default='vehicles/default.jpg', upload_to='vehicles'),
        ),
        migrations.AlterField(
            model_name='vehicletype',
            name='photo',
            field=models.ImageField(default='vehicles/default.jpg', upload_to='vehicletype'),
        ),
    ]
