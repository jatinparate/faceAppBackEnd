import os

from django.db import models


def get_upload_path(instance, filename):
    return 'images/' + instance.branch + '/' + instance.class_str + '/' + filename


class Image(models.Model):
    branch = models.CharField(max_length=10)
    class_str = models.CharField(max_length=5)
    time = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to=get_upload_path)



