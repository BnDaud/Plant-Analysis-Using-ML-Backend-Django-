from django.db import models

# Create your models here.


class MLModelInput(models.Model):
    name = models.CharField(max_length=200)
    sunlight = models.SmallIntegerField()
    windcurrent = models.SmallIntegerField()
    rainfall = models.SmallIntegerField()
    humidity = models.SmallIntegerField()
    phvalue = models.SmallIntegerField()
    temperature = models.SmallIntegerField()
    topography = models.CharField(max_length=200)
    soiltype = models.CharField(max_length=200)
    soiltexture = models.CharField(max_length=200)
    minerals = models.CharField(max_length=200)
    result = models.TextField(max_length=1000 , blank=True)


    def __str__(self) -> str:
        
        return self.name