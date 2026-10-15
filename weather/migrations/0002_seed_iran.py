import json
from pathlib import Path

from django.db import migrations


def seed_iran(apps, schema_editor):
    Country = apps.get_model("weather", "Country")
    Province = apps.get_model("weather", "Province")
    City = apps.get_model("weather", "City")
    path = Path(__file__).resolve().parents[1] / "data" / "iran_locations.json"
    locations = json.loads(path.read_text(encoding="utf-8"))

    iran, _ = Country.objects.get_or_create(
        name="ایران", defaults={"latitude": 32.4279, "longitude": 53.6880}
    )
    for item in locations:
        province, _ = Province.objects.get_or_create(
            country=iran,
            name=item["province"],
            defaults={"latitude": item["latitude"], "longitude": item["longitude"]},
        )
        City.objects.bulk_create(
            [City(province=province, name=city["name"], latitude=city["latitude"],
                  longitude=city["longitude"]) for city in item["cities"]],
            ignore_conflicts=True,
            batch_size=300,
        )


class Migration(migrations.Migration):
    dependencies = [("weather", "0001_initial")]
    operations = [migrations.RunPython(seed_iran, migrations.RunPython.noop)]
