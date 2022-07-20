from django.db import models
from django.utils import timezone

# Create your models here.


class meter_config(models.Model):
    meterGUID = models.CharField(max_length=36, primary_key=True,unique=True,null=False)
    meterName = models.TextField(default='表')
    belongLab=models.TextField(null=False)
    def __str__(self):
        return self.meterName

class meter_data(models.Model):
    meterGUID = models.CharField(max_length=36)
    timestamp= models.DateTimeField(auto_now_add=True)
    value = models.FloatField(default=-1.0)

class lab_config(models.Model):
    labName = models.TextField(default='实验室')
    def __str__(self):
        return self.labName

class ai_process(models.Model):
    pid = models.IntegerField(null=False)
    takeinVideo=models.TextField(null=False)
    belong2Meter=models.ForeignKey(meter_config,on_delete=models.CASCADE)
    previewImage=models.TextField(null=True)
