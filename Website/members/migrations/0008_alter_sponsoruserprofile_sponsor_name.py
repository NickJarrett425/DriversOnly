# Generated by Django 4.2.5 on 2023-11-06 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_remove_userprofile_sponsor_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsoruserprofile',
            name='sponsor_name',
            field=models.CharField(max_length=25),
        ),
    ]
