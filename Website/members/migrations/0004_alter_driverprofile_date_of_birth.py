# Generated by Django 4.2.5 on 2023-10-09 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_vehicle_driverprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
