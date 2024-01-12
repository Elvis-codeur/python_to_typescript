from django.db import models
# Create your models here.

class Mod(models.Model):
    w = models.CharField()



def retu(a,b,c,lkd = 23,lsppe = Mod, roel = "oieoe",*args,**kwargs) ->int:

    return models.CharField(max_length=20,verbose_name = "kooso",is_required = False)

class ModelTest1(models.Model):
    nom = models.CharField(max_length=20,verbose_name = "kooso",is_required = False)
    age = models.IntegerField("Elvis-age")
    key = models.ForeignKey(to = Mod)
    ml = str()
    pl = retu(2,3,4)

    class Meta:
        model = Mod 
        fields = ["eld","eld"]



class TestRestFrameWork(models.Model):
    name = models.CharField()
    age = models.IntegerField()
    