from django.shortcuts import render

from .models import City, Country, Province
from .jalali import jalali_date, jalali_datetime
from .services import WeatherUnavailable, get_weather


def _id(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def home(request):
    countries = Country.objects.all()
    country = Country.objects.filter(pk=_id(request.GET.get("country"))).first()
    if country is None:
        country = Country.objects.filter(name="ایران").first() or countries.first()

    provinces = Province.objects.filter(country=country) if country else Province.objects.none()
    province = provinces.filter(pk=_id(request.GET.get("province"))).first()
    if province is None:
        province = (provinces.filter(name="البرز").first() if country and country.name == "ایران" else None) or provinces.first()

    cities = City.objects.filter(province=province) if province else City.objects.none()
    city = cities.filter(pk=_id(request.GET.get("city"))).first()
    location = city or province or country

    weather = None
    updated_at = None
    error = None
    if location:
        try:
            weather = get_weather(location.latitude, location.longitude)
            updated_at = jalali_datetime(weather["current"]["time"])
            for day in weather["forecast"]:
                day["jalali_date"] = jalali_date(day["date"])
        except WeatherUnavailable:
            error = "ارتباط با سرویس هواشناسی برقرار نشد. کمی بعد دوباره تلاش کنید."
    else:
        error = "هنوز مکانی ثبت نشده است. ابتدا از پنل مدیریت کشور و استان اضافه کنید."

    return render(request, "weather/home.html", {
        "countries": countries, "country": country, "provinces": provinces,
        "province": province, "cities": cities, "city": city,
        "location": location, "weather": weather, "error": error,
        "updated_at": updated_at,
    })
