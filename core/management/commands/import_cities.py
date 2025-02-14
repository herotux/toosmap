import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from core.models import Province, County, City

class Command(BaseCommand):
    help = "Imports counties and cities from a JSON file"

    def handle(self, *args, **kwargs):
        with open("cities_sorted.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # **مرحله اول: ایمپورت شهرستان‌ها**
        for key, item in data.items():
            if item["is_county"]:  # فقط شهرستان‌ها
                province_id = item["province_id"]
                county_id = item["id"]
                name = item["name"]
                slug = (item["en_name"] or item["name"]).lower().replace(" ", "-")  # مقداردهی مطمئن به `slug`

                # بررسی و اصلاح تکراری بودن `slug`
                if County.objects.filter(slug=slug).exists():
                    slug = f"{slug}-{province_id}"

                # بررسی وجود مختصات معتبر
                lat = item["lat"]
                lon = item["lon"]
                if lat is not None and lon is not None:
                    try:
                        lat = float(lat)
                        lon = float(lon)
                        coordinates = Point(lon, lat)
                    except ValueError:
                        coordinates = None
                else:
                    coordinates = None

                try:
                    province = Province.objects.get(id=province_id)
                except Province.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"⚠️ استان با ID {province_id} پیدا نشد. شهرستان {name} رد شد."))
                    continue

                county, created = County.objects.update_or_create(
                    id=county_id,
                    defaults={"name": name, "slug": slug, "province": province, "coordinates": coordinates},
                )
                action = "ایجاد شد" if created else "بروزرسانی شد"
                self.stdout.write(self.style.SUCCESS(f"{action} شهرستان: {name}"))

        # **مرحله دوم: ایمپورت شهرها**
        for key, item in data.items():
            if not item["is_county"]:  # فقط شهرها
                county_id = item["county_id"]
                city_id = item["id"]
                name = item["name"]
                slug = (item["en_name"] or item["name"]).lower().replace(" ", "-")  # مقداردهی مطمئن به `slug`

                # بررسی و اصلاح تکراری بودن `slug`
                original_slug = slug
                counter = 1
                while City.objects.filter(slug=slug).exists():
                    slug = f"{original_slug}-{counter}"
                    counter += 1

                # بررسی وجود مختصات معتبر
                lat = item["lat"]
                lon = item["lon"]
                if lat is not None and lon is not None:
                    try:
                        lat = float(lat)
                        lon = float(lon)
                        coordinates = Point(lon, lat)
                    except ValueError:
                        coordinates = None
                else:
                    coordinates = None

                try:
                    county = County.objects.get(id=county_id)
                except County.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"⚠️ شهرستان با ID {county_id} برای شهر {name} پیدا نشد. رد شد."))
                    continue

                city, created = City.objects.update_or_create(
                    id=city_id,
                    defaults={"name": name, "slug": slug, "county": county, "coordinates": coordinates},
                )
                action = "ایجاد شد" if created else "بروزرسانی شد"
                self.stdout.write(self.style.SUCCESS(f"{action} شهر: {name}"))

        self.stdout.write(self.style.SUCCESS("✅ ایمپورت شهرستان‌ها و شهرها با موفقیت انجام شد."))