from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coordinates(models.Model):
    latitude = models.FloatField("عرض جغرافیایی", validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField("طول جغرافیایی", validators=[MinValueValidator(-180), MaxValueValidator(180)])

    class Meta:
        abstract = True


class Country(Coordinates):
    name = models.CharField("نام کشور", max_length=100, unique=True)

    class Meta:
        verbose_name = "کشور"
        verbose_name_plural = "کشورها"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Province(Coordinates):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="provinces", verbose_name="کشور")
    name = models.CharField("نام استان", max_length=100)
    image = models.ImageField("تصویر شاخص", upload_to="provinces/", blank=True)
    image_caption = models.CharField("توضیح کوتاه تصویر", max_length=200, blank=True)
    image_credit = models.CharField("عکاس/پدیدآورنده", max_length=200, blank=True)
    image_license = models.CharField("مجوز تصویر", max_length=80, blank=True)
    image_license_url = models.URLField("لینک مجوز تصویر", blank=True)
    image_source = models.URLField("صفحهٔ منبع تصویر", max_length=500, blank=True)

    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان‌ها"
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["country", "name"], name="unique_province_per_country")]

    def __str__(self):
        return self.name


class City(Coordinates):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities", verbose_name="استان")
    name = models.CharField("نام شهر", max_length=100)

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["province", "name"], name="unique_city_per_province")]

    def __str__(self):
        return self.name
