from django.db import models

# Create your models here.


class FileUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    datafile = models.FileField()