from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import City, Country, Province
from .services import WeatherUnavailable
from .jalali import jalali_date, jalali_datetime


SAMPLE_WEATHER = {
    "current": {"temperature_2m": 22, "relative_humidity_2m": 40,
                "wind_speed_10m": 8, "precipitation": 0, "apparent_temperature": 21,
                "time": "2026-10-15T12:00"},
    "description": "صاف و آفتابی", "icon": "bi-sun-fill", "forecast": [],
}


class HomeTests(TestCase):
    @patch("weather.views.get_weather", return_value=SAMPLE_WEATHER)
    def test_default_is_iran_and_alborz(self, get_weather):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["country"].name, "ایران")
        self.assertEqual(response.context["province"].name, "البرز")
        self.assertIsNone(response.context["city"])
        self.assertTrue(response.context["province"].image.name)
        self.assertContains(response, "سد امیرکبیر، معروف به سد کرج")
        get_weather.assert_called_once()

    @patch("weather.views.get_weather", return_value=SAMPLE_WEATHER)
    def test_city_from_another_province_is_ignored(self, get_weather):
        iran = Country.objects.get(name="ایران")
        alborz = Province.objects.get(country=iran, name="البرز")
        tehran = Province.objects.get(country=iran, name="تهران")
        other_city = City.objects.filter(province=tehran).first()
        response = self.client.get(reverse("home"), {
            "country": iran.pk, "province": alborz.pk, "city": other_city.pk,
        })
        self.assertIsNone(response.context["city"])
        get_weather.assert_called_once_with(alborz.latitude, alborz.longitude)


    @patch("weather.views.get_weather", side_effect=WeatherUnavailable)
    def test_api_failure_shows_a_message(self, get_weather):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ارتباط با سرویس هواشناسی برقرار نشد")

    def test_all_seeded_provinces_have_local_images(self):
        provinces = Province.objects.filter(country__name="ایران")
        self.assertEqual(provinces.count(), 31)
        self.assertTrue(all(province.image and province.image.storage.exists(province.image.name)
                            for province in provinces))
        self.assertTrue(all(province.image_caption for province in provinces))


class JalaliTests(TestCase):
    def test_gregorian_dates_are_displayed_in_jalali(self):
        self.assertEqual(jalali_date("2026-10-15"), "۱۴۰۵/۰۷/۲۳")
        self.assertEqual(jalali_datetime("2026-10-15T12:30"), "۱۴۰۵/۰۷/۲۳، ۱۲:۳۰")
