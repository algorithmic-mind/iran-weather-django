import json
from pathlib import Path

from django.db import migrations


def seed_license_urls(apps, schema_editor):
    Province = apps.get_model("weather", "Province")
    path = Path(__file__).resolve().parents[1] / "data" / "photo_credits.json"
    photos = json.loads(path.read_text(encoding="utf-8"))
    for name, photo in photos.items():
        Province.objects.filter(country__name="ایران", name=name).update(
            image_license_url=photo["license_url"]
        )


class Migration(migrations.Migration):
    dependencies = [("weather", "0005_province_image_license_url")]
    operations = [migrations.RunPython(seed_license_urls, migrations.RunPython.noop)]
