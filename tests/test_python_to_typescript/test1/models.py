from django.db import models

# Create your models here.

class Mod(models.Model):
    w = models.CharField()

class ModelTest1(models.Model):
    nom = models.CharField(max_length=20,verbose_name = "kooso",is_required = False)
    age = models.IntegerField("Elvis-age")
    key = models.ForeignKey(to = Mod)
    def retu():
        pass 
