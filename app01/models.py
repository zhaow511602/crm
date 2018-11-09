from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=32)

class UserInof(models.Model):
    user = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
