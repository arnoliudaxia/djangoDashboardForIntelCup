from django.db import models

# Create your models here.


class meter_config(models.Model):
    meterGUID = models.CharField(max_length=36, primary_key=True,unique=True,null=False)
    meterName = models.TextField(default='表')
    def __str__(self):
        return self.meterName

class meter_data(models.Model):
    meterGUID = models.CharField(max_length=36)
    timestamp= models.DateTimeField(auto_now_add=True)
    value = models.FloatField(default=-1.0)