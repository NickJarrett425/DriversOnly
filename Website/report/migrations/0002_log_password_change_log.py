# Generated by Django 4.2.6 on 2023-11-07 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Datestamp', models.DateTimeField(auto_now=True)),
                ('username', models.CharField(default='test', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='password_change_log',
            fields=[
                ('log_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='report.log')),
                ('password_change_type', models.BooleanField()),
            ],
            bases=('report.log',),
        ),
    ]
