# Generated by Django 2.2.5 on 2022-01-12 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_auto_20220112_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amenity',
            name='wltnqkr',
        ),
        migrations.RemoveField(
            model_name='facility',
            name='wltnqkr',
        ),
        migrations.RemoveField(
            model_name='houserule',
            name='wltnqkr',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='wltnqkr',
        ),
        migrations.RemoveField(
            model_name='room',
            name='wltnqkr',
        ),
        migrations.RemoveField(
            model_name='roomtype',
            name='wltnqkr',
        ),
    ]
