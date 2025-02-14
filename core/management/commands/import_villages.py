import json
import random
from django.core.management.base import BaseCommand
from core.models import Village, Province, County
from django.contrib.gis.geos import Point
from django.db import IntegrityError
from collections import defaultdict

class Command(BaseCommand):
    help = 'Import villages from JSON data'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['json_file']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                villages_data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'خطا در بارگذاری فایل: {str(e)}'))
            return

        Village.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('تمامی روستاها با موفقیت حذف شدند.'))

        slug_count = defaultdict(int)
        coordinate_cache = set()
        villages_to_create = []
        errors = []
        warnings = []

        # پیش پردازش اسلاگ‌ها
        for village in villages_data:
            if village.get('type') != 'village':
                continue

            original_slug = village['slug']
            slug_count[original_slug] += 1

            if slug_count[original_slug] > 1:
                village['unique_slug'] = f"{original_slug}-{village['county']}-{village['id']}"
            else:
                village['unique_slug'] = original_slug

        # پردازش اصلی
        for village in villages_data:
            if village.get('type') != 'village':
                continue

            try:
                # اعتبارسنجی فیلدهای ضروری
                required_fields = ['id', 'name', 'slug', 'coordinates', 'province', 'county']
                for field in required_fields:
                    if field not in village:
                        raise ValueError(f"فیلد ضروری '{field}' وجود ندارد")

                # دریافت موجودیت‌های مرتبط
                province = Province.objects.get(id=village['province'])
                county = County.objects.get(id=village['county'])

                # پردازش مختصات
                raw_coords = village['coordinates']
                point = None
                
                if isinstance(raw_coords, list) and len(raw_coords) == 2:
                    try:
                        lng = float(raw_coords[0])
                        lat = float(raw_coords[1])

                        # اعتبارسنجی محدوده جغرافیایی ایران
                        if not (44.0 <= lng <= 63.5) or not (25.0 <= lat <= 39.5):
                            raise ValueError("مختصات خارج از مرزهای ایران")

                        # بررسی تکراری بودن مختصات
                        coord_key = (round(lat, 4), round(lng, 4))
                        if coord_key in coordinate_cache:
                            warnings.append(f"مختصات تکراری برای روستا {village['id']} - {village['name']}")
                            # ایجاد جابجایی تصادفی
                            lat += random.uniform(-0.0001, 0.0001)
                            lng += random.uniform(-0.0001, 0.0001)
                            
                        coordinate_cache.add(coord_key)
                        point = Point(lng, lat)

                    except (TypeError, ValueError) as e:
                        raise ValueError(f"مختصات نامعتبر: {str(e)}")

                # ایجاد شیء روستا (بدون فیلدهای district و rural_district)
                village_obj = Village(
                    id=village['id'],
                    name=village['name'],
                    slug=village['unique_slug'],
                    coordinates=point,
                    province=province,
                    county=county
                )

                villages_to_create.append(village_obj)

            except Province.DoesNotExist:
                errors.append(f"استان با شناسه {village['province']} یافت نشد")
            except County.DoesNotExist:
                errors.append(f"شهرستان با شناسه {village['county']} یافت نشد")
            except Exception as e:
                errors.append(f"خطا در پردازش روستا {village['id']}: {str(e)}")

        # ذخیره دسته‌ای
        if villages_to_create:
            try:
                Village.objects.bulk_create(villages_to_create)
                self.stdout.write(self.style.SUCCESS(f'با موفقیت {len(villages_to_create)} روستا وارد شدند.'))
            except IntegrityError as e:
                errors.append(f"خطای یکپارچگی دیتابیس: {str(e)}")

        # نمایش هشدارها
        if warnings:
            self.stdout.write(self.style.WARNING('\nهشدارها:'))
            for warn in warnings:
                self.stdout.write(self.style.WARNING(warn))

        # نمایش خطاها
        if errors:
            self.stdout.write(self.style.ERROR('\nخطاها:'))
            for error in errors:
                self.stdout.write(self.style.ERROR(error))