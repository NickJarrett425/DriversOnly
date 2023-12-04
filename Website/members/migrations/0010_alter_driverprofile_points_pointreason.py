# Generated by Django 4.2.5 on 2023-12-04 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0009_sponsorlist_point_conversion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverprofile',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='PointReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_amt', models.IntegerField(default=0)),
                ('point_reason', models.TextField(blank=True, max_length=250)),
                ('is_add', models.BooleanField(default=True, verbose_name='point change type')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.driverprofile')),
                ('sponsor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.sponsoruserprofile')),
            ],
        ),
    ]
