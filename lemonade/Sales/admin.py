from django.contrib import admin
from .models import *

# Register your models here.


class SaleAdmin(admin.ModelAdmin):
    class Meta:
        Model=Sale


admin.site.register(Lemonade)
admin.site.register(Staff)
admin.site.register(Order)
admin.site.register(LemonadeSet)
admin.site.register(Sale)
