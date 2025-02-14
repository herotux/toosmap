from rest_framework import serializers
from .models import JobLinks, County, user, Province, City, category_job, job, role, role_user, Village, JobHours, TimeSlot
import uuid
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP
from django.contrib.gis.db import models as gis_models
import random
from django.contrib.gis.geos import Point







class EmptyStringToNoneIntegerField(serializers.IntegerField):
    def to_internal_value(self, data):
        if data == '':
            return None
        return super().to_internal_value(data)

    def run_validators(self, value):
        # اعتبارسنجی را فقط زمانی انجام بده که مقدار None نباشد
        if value is not None:
            super().run_validators(value)




class UserSerializer(serializers.ModelSerializer):
    coordinates = serializers.JSONField(
        write_only=True,
        required=False,
        allow_null=True,
        help_text='{"type": "Point", "coordinates": [lon, lat]}'
    )
    province = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        help_text="نام استان (اختیاری)"
    )
    city = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="نام شهر (اختیاری)"
    )

    district_id = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="نام منطقه (اختیاری)"
    )
    county = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        help_text="نام شهرستان (اختیاری)"
    )
    village = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="نام شهرستان (اختیاری)"
    )
    role = serializers.CharField(
        write_only=True,
        allow_null=False,
        required=True)

    year = EmptyStringToNoneIntegerField(
        required=False,
        allow_null=True,
        min_value=1300,
        max_value=1500
    )
    month = EmptyStringToNoneIntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        max_value=12
    )
    day = EmptyStringToNoneIntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        max_value=31
    )
    is_mobile_confirmed = serializers.BooleanField(required=False)
    
    class Meta:
        model = user
        fields = [
            'coordinates', 'first_name', 'last_name', 'mobile', 'password', 'email', 'national_code',
            'national', 'province', 'county', 'city', 'village', 'district_id', 'year', 'month', 'day', 
            'created_by_admin', 'role','is_mobile_confirmed'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'national_code': {'required': False, 'allow_blank': True},
            'email': {'required': False, 'allow_blank': True}
        }

    def validate_coordinates(self, coordinates_data):
        if coordinates_data is None:
            return None

        if not isinstance(coordinates_data, dict):
            raise serializers.ValidationError("coordinates باید یک دیکشنری باشد.")

        required_keys = ['type', 'coordinates']
        if not all(key in coordinates_data for key in required_keys):
            raise serializers.ValidationError(f"coordinates باید شامل کلیدهای {required_keys} باشد.")

        if coordinates_data['type'] != 'Point':
            raise serializers.ValidationError("نوع coordinates باید Point باشد.")

        coordinates = coordinates_data['coordinates']
        if not isinstance(coordinates, list) or len(coordinates) != 2:
            raise serializers.ValidationError("coordinates باید یک لیست با دو عدد (طول و عرض جغرافیایی) باشد.")

        try:
            lon = float(coordinates[0])  # تبدیل به عدد
            lat = float(coordinates[1])  # تبدیل به عدد
        except (ValueError, TypeError):
            raise serializers.ValidationError("طول و عرض جغرافیایی باید عددی باشند.")

        return {"type": "Point", "coordinates": [lon, lat]}





    def generate_unique_user_code(self, username):
        # استفاده از 4 رقم آخر موبایل + 6 رقم تصادفی
        random_part = random.randint(100000, 999999)
        code = f"{username[-4:]}{random_part}"

        # بررسی یونیک بودن در دیتابیس
        while user.objects.filter(user_code=code).exists():
            random_part = random.randint(100000, 999999)
            code = f"{username[-4:]}{random_part}"

        return code



    def create(self, validated_data):
        try:
            village_name = validated_data.pop('village', None)
            role_name = validated_data.pop('role')
            is_mobile_confirmed = validated_data.pop('is_mobile_confirmed', False)
            coordinates_data = validated_data.pop('coordinates', None)
            province_name = validated_data.pop('province', None)
            county_name = validated_data.pop('county', None)
            city_name = validated_data.pop('city', None)
            district_id = validated_data.pop('district_id', None)

            province = Province.objects.filter(name=province_name).first()
            if not province:
                raise serializers.ValidationError("استان انتخاب شده معتبر نیست")

            county = County.objects.filter(name=county_name, province=province).first()
            if not county:
                raise serializers.ValidationError("شهرستان انتخاب شده معتبر نیست")
            

            city = None
            if city_name:
                city = City.objects.filter(name=city_name, county=county).first()
                if not city:
                    raise serializers.ValidationError("شهر انتخاب شده معتبر نیست")
            

            village = None
            if village_name:
                village = Village.objects.filter(name=village_name, county=county).first()
                if not village:
                    raise serializers.ValidationError("روستای انتخاب شده معتبر نیست")
                

            username = validated_data['mobile']
            if user.objects.filter(username=username).exists():
                raise serializers.ValidationError("کاربری با این شماره موبایل از قبل وجود دارد")

            validated_data.update({
                'province_id': province.id,
                'county_id': county.id,
                'city_id': city.id if city else None,
                'village_id': village.id if village else None,
                'district_id': district_id if district_id else None,
                'username': username,
                'user_code': self.generate_unique_user_code(username),
                'is_mobile_confirmed': is_mobile_confirmed
            })

            new_user = user.objects.create_user(**validated_data)

            if coordinates_data:
                new_user.coordinates = Point(
                    coordinates_data['coordinates'],
                    srid=4326
                )
                new_user.save()

            # role_instance = role.objects.get(name=role_name)
            role_instance = role.objects.filter(name=role_name).first()
            if not role_instance:
                raise serializers.ValidationError("نقش انتخاب شده معتبر نیست")
            role_user.objects.create(user=new_user, role=role_instance)

            return new_user
        except Exception as e:
            import traceback
            print('Error:', str(e))
            print('Traceback:', traceback.format_exc())
            raise serializers.ValidationError(f"خطا در ایجاد کاربر: {str(e)}")

    




class CategoryJobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = category_job
        fields = [
            'name', 'slug', 'label', 'icon', 'image', 'banner', 'meta_keywords',
            'meta_description', 'parent', 'has_slider', 'sort_order', 'view_counts', 'status'
        ]
        extra_kwargs = {
            'icon': {'required': False},  # فایل‌ها اختیاری هستند
            'image': {'required': False},
            'banner': {'required': False},
            'label': {'required': False},
            'meta_keywords': {'required': False},
            'meta_description': {'required': False},
            'parent': {'required': False},
            'has_slider': {'required': False},
            'sort_order': {'required': False},
            'view_counts': {'required': False},
            'status': {'required': False},
        }


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = job
        fields = '__all__'  # Ensure user_id is included in these fields


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time']






class JobHoursSerializer(serializers.ModelSerializer):
    shifts = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = JobHours
        fields = ['day', 'shifts']

    def create(self, validated_data):
        shifts_data = validated_data.pop('shifts')
        job_hour = JobHours.objects.create(**validated_data)
        for shift in shifts_data:
            TimeSlot.objects.create(
                job_hour=job_hour,
                start_time=shift['start'],
                end_time=shift['end']
            )
        return job_hour

class JobLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLinks
        fields = ['website', 'telegram', 'instagram', 'robika', 'eitaa', 'bale']