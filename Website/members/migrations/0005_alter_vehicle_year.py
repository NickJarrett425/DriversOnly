# Generated by Django 4.2.5 on 2023-10-09 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_alter_driverprofile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='year',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
