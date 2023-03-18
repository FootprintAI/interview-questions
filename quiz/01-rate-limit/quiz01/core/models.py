from django.db import models

# Create your models here.
class CoreModel(models.Model):
    song = models.TextField()
    singer = models.TextField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     db_table = "coremodel"