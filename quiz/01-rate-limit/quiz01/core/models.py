from django.db import models

# Create your models here.

# class Customer_ID_Model(models.Model):
#     customer_ID = models.TextField(primary_key=True)
#     # other customer info...
#     class Meta:
#         db_table = "Customer_ID_Model"

class GET_Model(models.Model):
    customer_ID = models.TextField(primary_key=True)
    path = models.TextField(default = 'n/a')
    Limit = models.IntegerField(default=100)
    Remaining = models.IntegerField(default=100)
    Reset = models.IntegerField(default=1)
    RetryAt = models.IntegerField(default=0)
    upData = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "GET_Model"

class POST_Model(models.Model):
    customer_ID = models.TextField(primary_key=True)
    path = models.TextField(default = 'n/a')
    Limit = models.IntegerField(default=1)
    Remaining = models.IntegerField(default=1)
    Reset = models.IntegerField(default=1)
    RetryAt = models.IntegerField(default=0)
    upData = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "POST_Model"
