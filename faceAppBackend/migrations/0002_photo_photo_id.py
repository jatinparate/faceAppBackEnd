# Generated by Django 2.2.7 on 2020-01-05 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceAppBackend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='photo_id',
            field=models.IntegerField(default=0),
        ),
    ]
