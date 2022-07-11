from django.db import models

# Create your models here.


class meter_config(models.Model):
    meterGUID = models.CharField(max_length=36, primary_key=True)
    meterName = models.TextField(default='表')
    def __str__(self):
        return self.meterName