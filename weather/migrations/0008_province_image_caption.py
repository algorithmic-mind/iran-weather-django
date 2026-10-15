import json
from pathlib import Path

from django.db import migrations, models


def seed_captions(apps, schema_editor):
    Province = apps.get_model("weather", "Province")
    path = Path(__file__).resolve().parents[1] / "data" / "province_captions.json"
    captions = json.loads(path.read_text(encoding="utf-8"))
    for name, caption in captions.items():
        Province.objects.filter(country__name="ایران", name=name).update(image_caption=caption)


class Migration(migrations.Migration):
    dependencies = [("weather", "0007_alter_province_image_source")]
    operations = [
        migrations.AddField(
            model_name="province",
            name="image_caption",
            field=models.CharField(blank=True, max_length=200, verbose_name="توضیح کوتاه تصویر"),
        ),
        migrations.RunPython(seed_captions, migrations.RunPython.noop),
    ]
