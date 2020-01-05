from django.db import models


class Photo (models.Model):
    branch = models.CharField(max_length=10)
    class_str = models.CharField(max_length=5)
    time = models.DateTimeField(auto_now_add=True)
    photo_id = models.IntegerField(default=0)
    file = models.FileField(upload_to='photos/')

