from django.contrib import admin

from .models import City, Country, Province


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "latitude", "longitude", "image", "image_caption")
    list_filter = ("country",)
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "latitude", "longitude")
    list_filter = ("province__country",)
    search_fields = ("name", "province__name")
