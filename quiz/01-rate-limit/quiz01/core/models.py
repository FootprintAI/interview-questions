from django.db import models

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=250)

    price = models.CharField(max_length=250)

    color = models.CharField(max_length=250)

    weight = models.CharField(max_length=250)