# Generated by Django 2.2.7 on 2020-01-05 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faceAppBackend', '0003_auto_20200105_1518'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='photo_id',
        ),
    ]