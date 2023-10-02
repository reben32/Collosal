from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from chapter_3.models import Seller
from chapter_3.models import Engine, Seller, Vehicle, VehicleModel
# Register your models here.


class SellerAdmin(ModelAdmin):
    pass

class SellerAdmin(UserAdmin):
    pass

@admin.register(Seller)
class SellerAdmin(UserAdmin):
    pass