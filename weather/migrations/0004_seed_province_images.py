import json
from pathlib import Path

from django.db import migrations


def seed_images(apps, schema_editor):
    Province = apps.get_model("weather", "Province")
    path = Path(__file__).resolve().parents[1] / "data" / "photo_credits.json"
    photos = json.loads(path.read_text(encoding="utf-8"))
    for name, photo in photos.items():
        Province.objects.filter(country__name="ایران", name=name).update(
            image=photo["file"],
            image_credit=photo["author"],
            image_license=photo["license"],
            image_source=photo["source"],
        )


class Migration(migrations.Migration):
    dependencies = [("weather", "0003_province_image_province_image_credit_and_more")]
    operations = [migrations.RunPython(seed_images, migrations.RunPython.noop)]
