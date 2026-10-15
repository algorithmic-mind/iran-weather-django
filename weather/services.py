import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.core.cache import cache


API_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherUnavailable(Exception):
    pass


def weather_description(code, is_day=True):
    """Return a Persian description and a Bootstrap Icons class for a WMO code."""
    if code == 0:
        return ("صاف و آفتابی", "bi-sun-fill") if is_day else ("آسمان صاف", "bi-moon-stars-fill")
    if code == 1:
        return ("عمدتاً صاف", "bi-sun") if is_day else ("عمدتاً صاف", "bi-moon-stars")
    if code == 2:
        return ("نیمه‌ابری", "bi-cloud-sun-fill") if is_day else ("نیمه‌ابری", "bi-cloud-moon-fill")
    if code == 3:
        return "ابری", "bi-cloud-fill"
    if code in (45, 48):
        return "مه‌آلود", "bi-cloud-fog2-fill"
    if code in (51, 53, 55, 56, 57):
        return "نم‌نم باران", "bi-cloud-drizzle-fill"
    if code in (61, 63, 65, 66, 67):
        return "بارانی", "bi-cloud-rain-heavy-fill"
    if code in (71, 73, 75, 77, 85, 86):
        return "برفی", "bi-cloud-snow-fill"
    if code in (80, 81, 82):
        return "رگبار باران", "bi-cloud-rain-fill"
    if code in (95, 96, 97, 99):
        return "رعد و برق", "bi-cloud-lightning-rain-fill"
    return "وضعیت نامشخص", "bi-cloud"


def get_weather(latitude, longitude):
    """Fetch current conditions and three daily forecasts with a short cache."""
    key = f"weather:{latitude:.5f}:{longitude:.5f}"
    cached = cache.get(key)
    if cached is not None:
        return cached

    query = urlencode({
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,is_day",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": 3,
        "timezone": "Asia/Tehran",
    })
    try:
        with urlopen(f"{API_URL}?{query}", timeout=8) as response:
            data = json.load(response)
        current = data["current"]
        daily = data["daily"]
        description, icon = weather_description(current["weather_code"], current.get("is_day", 1) == 1)
        forecast = []
        for day, code, maximum, minimum, rain in zip(
            daily["time"], daily["weather_code"], daily["temperature_2m_max"],
            daily["temperature_2m_min"], daily["precipitation_sum"], strict=True,
        ):
            day_description, day_icon = weather_description(code)
            forecast.append({"date": day, "description": day_description, "icon": day_icon,
                             "max": maximum, "min": minimum, "precipitation": rain})
        weather = {"current": current, "description": description, "icon": icon,
                   "forecast": forecast}
    except (HTTPError, URLError, TimeoutError, ValueError, KeyError, TypeError) as exc:
        raise WeatherUnavailable("دریافت اطلاعات هواشناسی ممکن نشد.") from exc

    cache.set(key, weather, 600)
    return weather
