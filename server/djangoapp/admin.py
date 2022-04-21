from django.contrib import admin
from .models import CarDealer,DealerReview,CarModel,CarMake
# Register your models here.

# CarModelInline class

# CarModelAdmin class

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register models here


admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel)
