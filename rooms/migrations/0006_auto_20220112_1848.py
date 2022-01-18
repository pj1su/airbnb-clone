# Generated by Django 2.2.5 on 2022-01-12 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_auto_20220112_1805'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenity',
            name='wltnqkr',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='facility',
            name='wltnqkr',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='houserule',
            name='wltnqkr',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='photo',
            name='wltnqkr',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='room',
            name='wltnqkr',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='wltnqkr',
            field=models.TextField(blank=True, default=''),
        ),
    ]
