# Generated by Django 4.2.5 on 2023-11-02 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_application_is_approved_application_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
