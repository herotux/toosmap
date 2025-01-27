from rest_framework import serializers
from .models import user, Province, City, category_jobs, job, role, role_user
import uuid
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP


class UserSerializer(serializers.ModelSerializer):
    province = serializers.CharField(write_only=True)
    city = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)  # اضافه کردن فیلد نقش

    class Meta:
        model = user
        fields = [
            'first_name', 'last_name', 'mobile', 'password', 'email', 'national_code',
            'national', 'province', 'city', 'region', 'year', 'month', 'day', 'created_by_admin', 'role', 'lat', 'lng'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_lat(self, value):
        if value:
            return Decimal(value).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        return value

    def validate_lng(self, value):
        if value:
            return Decimal(value).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        return value

    def create(self, validated_data):
        province_name = validated_data.pop('province')
        city_name = validated_data.pop('city')
        role_name = validated_data.pop('role')

        province = Province.objects.get(name=province_name)
        city = City.objects.get(name=city_name)

        validated_data['province_id'] = province.id
        validated_data['city_id'] = city.id
        validated_data['username'] = validated_data['mobile']
        validated_data['user_code'] = f"{validated_data['mobile']}-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        new_user = user.objects.create_user(**validated_data)

        role_instance = role.objects.get(name=role_name)
        role_user.objects.create(user=new_user, role=role_instance)

        return new_user
    




class CategoryJobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = category_jobs
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
        fields = '__all__'