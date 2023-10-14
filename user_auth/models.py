from django.db import models

# Create your models here.
class Session(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=500,blank=False, default='')   