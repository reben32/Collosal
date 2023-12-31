from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator,MinMoneyValidator
from django.db.models.functions import Lower
from django.contrib.auth.models import AbstractUser

    
# Create your models here.
YESNO_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)

MAKE_CHOICES = (
    (0, '------'),
    (1, 'Buick'),
    (2, 'Cadillac'),
    (3, 'Chevrolet'),
    (4, 'Ford'),
    (5, 'GMC'),
    (6, 'Chrysler'),
    (7, 'Dodge'),
    (8, 'Jeep'),
    (9, 'Lincoln'),
    (10, 'Tesla'),
)
class VehicleModel (models.Model):
    name = models.CharField(verbose_name = 'Model', max_length = 75, unique = True, blank = True, null = True,)
    make = models.PositiveIntegerField(choices = MAKE_CHOICES, verbose_name = 'Make/Manufacturer', blank = True, null = True,)
    class Meta:
        verbose_name = 'Vehicle Model'
        verbose_name_plural = 'Vehicle Models'
        ordering = ['-name']
        indexes = [ models.Index(fields=['name']),
                    models.Index(fields = ['-name'], name = 'desc_name_idx'),
                    models.Index(Lower('name').desc(), name = 'lower_name_idx') ]
        
        
class Engine(models.Model):
    name = models.CharField(verbose_name = 'Engine', max_length = 75, blank = True, null = True,)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete = models.CASCADE, verbose_name = 'Model', related_name = 'model_engine', blank = True, null = True,)

class BuickVehicleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(make=1)
class ChevyVehicleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(make=3)
class Vehicle (models.Model):
    # Place Model Fields Here
    vin = models.CharField( verbose_name = 'VIN', max_length = 17, unique = True, blank = True, null = True,)   
    sold = models.BooleanField(verbose_name = 'Sold?', choices = YESNO_CHOICES, default = False, blank = True, null = True,)
    price = MoneyField(max_digits = 19, decimal_places = 2, default_currency = 'USD', null = True,validators = [ MinMoneyValidator({'EUR': 500, 'USD': 400}),MaxMoneyValidator({'EUR': 500000, 'USD': 400000}),])
    vehicle_model = models.ForeignKey(VehicleModel, on_delete = models.CASCADE, verbose_name = 'Model', related_name = 'model_vehicle', blank = True, null = True,)
    engine = models.ForeignKey(Engine, on_delete = models.CASCADE, verbose_name = 'Engine', related_name = 'engine_vehicle', blank = True, null = True,)
    make = models.PositiveIntegerField(choices = MAKE_CHOICES, verbose_name = 'Vehicle Make/Brand', blank = True,null = True,)
   
    # The Default Model Manager
    objects = models.Manager()
    
    # The Buick Specific Manager
    buick_objects = BuickVehicleManager()
    
    # The Chevy Specific Manager
    chevy_objects = ChevyVehicleManager()
    
    # Place Meta Class and Model Methods Here
    def __str__(self):
        MAKE_CHOICES_DICT = dict(MAKE_CHOICES)
        return MAKE_CHOICES_DICT[self.make] + ' ' + self.model.name
    
    def full_vehicle_name(self):
        return self.__str__() + ' - ' + self.engine.name
    
    @property
    def fullname(self):
        return self.__str__() + ' - ' + self.engine.name

class engine2(models.Model):
    name = models.CharField(verbose_name = 'Engine', max_length = 75, blank = True, null = True,)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete = models.CASCADE, verbose_name = 'Model', related_name = 'model_engine2', blank = True, null = True,)
    class Meta:
        abstract = True
        db_table = 'chapter_3_practice_engine'
        ordering = ['name',]
        verbose_name = 'Practice Engine'
        verbose_name_plural = 'Practice Engines'

class engine3(engine2):
    other_name = models.CharField(verbose_name = 'Other Engine Name', max_length = 75, blank = True, null = True,)
    
class Seller(AbstractUser):
    name = models.CharField(verbose_name = 'Seller Name', max_length = 150, blank = True, null = True,)
    vehicles = models.ManyToManyField(Vehicle, verbose_name = 'Vehicles', related_name = 'vehicle_sellers', related_query_name = 'vehicle_seller', blank = True,)
