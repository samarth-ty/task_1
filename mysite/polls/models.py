from lib2to3.pgen2 import driver
from django.db import models

class Info(models.Model):
    drive_link = models.URLField(default="default is null")

    def __str__(self):
        return self.drive_link

        