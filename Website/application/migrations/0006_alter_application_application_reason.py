# Generated by Django 4.2.5 on 2023-11-03 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_alter_application_application_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='application_reason',
            field=models.TextField(blank=True, max_length=250),
        ),
    ]
