import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Polygon
from core.models import District, County

class Command(BaseCommand):
    help = "ایمپورت مناطق شهرستان تهران از فایل GeoJSON"

    def add_arguments(self, parser):
        parser.add_argument("geojson_file", type=str, help="مسیر فایل GeoJSON مناطق شهرستان تهران")

    def handle(self, *args, **options):
        geojson_file = options["geojson_file"]

        with open(geojson_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        county, _ = County.objects.get_or_create(name="تهران", defaults={"slug": "tehran"})

        count = 0
        for feature in data.get("features", []):
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            name = properties.get("name")
            coordinates = geometry.get("coordinates")

            if not name or not coordinates:
                self.stdout.write(self.style.WARNING(f"Skipping invalid feature: {properties}"))
                continue

            # تبدیل مختصات به Polygon
            polygon = Polygon(coordinates[0])

            # ایجاد یا بروزرسانی منطقه
            district, created = District.objects.update_or_create(
                name=name,
                county=county,
                defaults={"geometry": polygon}
            )

            count += 1
            self.stdout.write(self.style.SUCCESS(f"{'Created' if created else 'Updated'}: {district.name}"))

        self.stdout.write(self.style.SUCCESS(f"✅ {count} منطقه وارد شد!"))