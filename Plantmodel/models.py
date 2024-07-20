from django.db import models

# Create your models here.


class MLModelInput(models.Model):
    name = models.CharField(max_length=200)
    sunlight = models.FloatField()
    windcurrent = models.FloatField()
    rainfall = models.FloatField()
    humidity = models.FloatField() # there is mis naming here humidity stands for Carbondioxide
    phvalue = models.FloatField()
    temperature = models.FloatField()
    topography = models.CharField(max_length=200)
    soiltype = models.CharField(max_length=200)
    #soiltexture = models.CharField(max_length=200)
    minerals =models.FloatField()
    result = models.TextField(max_length=1000 , blank=True)

    def __str__(self) -> str:
        
        return self.name