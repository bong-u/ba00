from django.db import models

class Musician(models.Model):
    
    name = models.CharField(max_length=30)
    value = models.IntegerField(primary_key=True)
    recent = models.IntegerField()
    image = models.URLField()