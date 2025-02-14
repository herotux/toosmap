import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from core.models import Province

class Command(BaseCommand):
    help = "Imports provinces from a JSON file"

    def handle(self, *args, **kwargs):
        # خواندن فایل JSON
        with open("provinces.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, province_data in data.items():
            name = province_data["name"]
            slug = province_data["en_name"].lower().replace(" ", "-")  # تبدیل نام انگلیسی به slug
            lat = float(province_data["lat"])
            lon = float(province_data["lon"])
            coordinates = Point(lon, lat)  # مختصات در فرمت (X, Y) یعنی (Longitude, Latitude)

            # ایجاد یا به‌روزرسانی استان در پایگاه داده
            province, created = Province.objects.update_or_create(
                id=province_data["id"],  # استفاده از ID موجود در JSON
                defaults={"name": name, "slug": slug, "coordinates": coordinates},
            )

            action = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{action} province: {name}"))

        self.stdout.write(self.style.SUCCESS("Provinces import completed successfully."))