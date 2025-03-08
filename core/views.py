import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import setting, Village, user, role_user, category_job, Province, City, job, role, County, JobHours, TimeSlot
from django.core.mail import send_mail  # For sending OTP
from django.contrib.auth import authenticate, login
import random
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from .forms import UserForm, JobForm, JobHoursForm, TimeSlotForm
from rest_framework import status
from .serializers import JobSerializerForFlutter, VillageSerializer, ProvinceSerializer, UserSerializer, CategoryJobsSerializer, JobLinksSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from django.contrib.auth import logout
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from .serializers import CountySerializer, CitySerializer, DistrictSerializer, CategoryJobSerializer, JobHoursSerializer, TimeSlotSerializer, JobSerializer, PlaceSerializer
from rest_framework.decorators import api_view
from django.db import IntegrityError
from rest_framework import permissions
from .decorators import role_required
from rest_framework import viewsets
from .models import Place, job
from django.db.models import Count
import logging

logger = logging.getLogger(__name__)


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # بررسی کنید که کاربر احراز هویت شده است
        if not request.user.is_authenticated:
            return False

        # بررسی کنید که کاربر دارای نقش admin است
        return role_user.objects.filter(user=request.user, role__name='admin').exists()
    


def get_categories_hierarchically(categories, parent=None, prefix=''):
    """
    تابع بازگشتی برای تولید لیست سلسله‌مراتبی دسته‌ها
    """
    result = []
    for category in categories.filter(parent=parent):
        full_name = f"{prefix}/{category.name}" if prefix else category.name
        result.append((category.id, full_name))
        result.extend(get_categories_hierarchically(categories, parent=category, prefix=full_name))
    return result




@role_required('admin')
def admin_dashboard(request):
    jobcount = job.objects.count()
    usercount = user.objects.count()
    catcount = category_job.objects.count()

    user_info = {
        'name': request.user.username,
        'role': role_user.objects.filter(user=request.user).first().role.name
    }
    return render(request, 'admin_user/dashboard.html', {'user_info': user_info,'jobcount':jobcount,'usercount':usercount,'catcount':catcount})






def register(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        entered_otp = request.POST['otp']

        if password == confirm_password:
            # Check if the mobile number already exists
            if user.objects.filter(username=mobile_number).exists():
                # If it exists, log the user in
                user_instance = user.objects.get(username=mobile_number)
                login(request, user_instance)
                return redirect('home')  # Redirect to home page
            else:
                # Logic to send OTP to the mobile number
                otp = request.session.get('otp')
                if entered_otp == str(otp):
                    user_instance = user.objects.create_user(username=mobile_number, password=password, mobile=mobile_number)
                    login(request, user_instance)
                    return redirect('home')  # Redirect to home page
                else:
                    return render(request, 'registration/register_with_otp.html', {'error': 'Invalid OTP.'})
        else:
            return render(request, 'registration/register_with_otp.html', {'error': 'Passwords do not match.'})

    return render(request, 'registration/register_with_otp.html')



def login_view(request):
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        user_instance = user.objects.filter(username=mobile_number).first()
        
        if user_instance:
            # If user exists, prompt for password
            return render(request, 'registration/login_password.html', {'mobile_number': mobile_number})
        else:
            # If user does not exist, generate OTP
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            print(otp)  # Print OTP for debugging
            return redirect('register')

    next_url = request.GET.get('next')
    return render(request, 'registration/login.html', {'next': next_url})



def verify_password(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        user_instance = user.objects.filter(username=mobile_number).first()

        if user_instance and user_instance.check_password(password):
            login(request, user_instance)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                role = role_user.objects.filter(user=request.user).first().role.name
                if role == 'admin':
                    return redirect('admin_dashboard')
                elif role == 'seller':
                    return redirect('seller_dashboard')
                else:
                    return redirect('user_dashboard')
        else:
            return render(request, 'registration/login_password.html', {'mobile_number': mobile_number, 'error': 'Invalid password.'})

    next_url = request.GET.get('next')
    return render(request, 'registration/login_password.html', {'next': next_url})


def otp_login(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        otp = request.session.get('otp')
        if otp and request.POST['otp'] == str(otp):
            user_instance = user.objects.get(username=mobile_number)
            login(request, user_instance)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                role = role_user.objects.filter(user=request.user).first().role.display_name
                if role == 'admin':
                    return redirect('admin_dashboard')
                elif role == 'seller':
                    return redirect('seller_dashboard')
                else:
                    return redirect('user_dashboard')
        else:
            return render(request, 'registration/login_otp.html', {'error': 'Invalid OTP.'})

    return render(request, 'registration/login_otp.html')



def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if entered_otp == str(request.session.get('otp')):
            # OTP is correct, register the user
            mobile_number = request.session.get('mobile_number')
            password = request.POST['password']
            user_instance = user.objects.create_user(username=mobile_number, password=password, mobile=mobile_number)
            login(request, user_instance)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('user_dashboard')  # Redirect to user dashboard
        else:
            return render(request, 'registration/verify_otp.html', {'error': 'Invalid OTP.'})
    return render(request, 'registration/verify_otp.html')


# Dashboard views


@role_required('seller')
@login_required
def seller_dashboard(request):
    user_info = {
        'name': request.user.username,
        'role': role_user.objects.filter(user=request.user).first().role.display_name
    }
    return render(request, 'seller/dashboard.html', {'user_info': user_info})

@login_required
def user_dashboard(request):
    user_info = {
        'name': request.user.username,
        'role': role_user.objects.filter(user=request.user).first().role.display_name
    }
    return render(request, 'user_dashboard.html', {'user_info': user_info})


def home(request):
    return render(request, 'main/home.html')


@role_required('admin')
def list_users(request):
    records_per_page = request.GET.get('records_per_page', 10)
    
    # شرط‌های فیلتر کردن
    users = user.objects.filter(
        Q(is_mobile_confirmed=True) | Q(created_by_admin=True)  # موبایل تایید شده یا توسط مدیر اضافه شده
    ).filter(active=True).order_by('created_at')  # فقط کاربران فعال

    # Fetch roles for each user
    user_roles = {user.id: role_user.objects.filter(user=user).first().role.display_name for user in users}

    paginator = Paginator(users, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_user/users_list.html', {'page_obj': page_obj, 'user_roles': user_roles})



@role_required('admin')
def list_categories(request):
    search_query = request.GET.get('search', '')
    records_per_page = request.GET.get('records_per_page', '10')
    
    try:
        records_per_page = int(records_per_page)
    except ValueError:
        records_per_page = 10

    # فیلتر اصلی با شرایط جستجو
    categories = category_job.objects.filter(parent=None)
    
    if search_query:
        categories = categories.filter(name__icontains=search_query)
    
    categories = categories.order_by('sort_order')

    paginator = Paginator(categories, records_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # افزودن زیرمجموعه‌ها
    for category in page_obj:
        category.subcategories = category_job.objects.filter(parent=category).order_by('sort_order')

    return render(request, 'admin_user/categories.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'records_per_page': records_per_page
    })



class ProvinceCityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        provinces = Province.objects.all()
        provinces_data = []
        for province in provinces:
            cities = City.objects.filter(province=province)
            cities_data = [{"name": city.name, "lat": city.lat, "lng": city.lng} for city in cities]
            provinces_data.append({
                "name": province.name,
                "cities": cities_data
            })
        return Response(provinces_data)

def map_view(request):
    return render(request, 'map/map.html')
    

@role_required('admin')
def add_category(request):
    categories = category_job.objects.all().order_by('sort_order')
    hierarchical_categories = get_categories_hierarchically(categories)
    print("Hierarchical Categories:", hierarchical_categories)
    return render(request, 'admin_user/add_category.html',{'categories': hierarchical_categories})




@role_required('admin')
def delete_category(request, category_id):
    category = get_object_or_404(category_job, id=category_id)
    category.delete()
    return redirect('list_categories')



# class MapDataLazyLoadAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         # دریافت پارامترهای جغرافیایی (محدوده و zoom level) از درخواست
#         north = float(request.GET.get('north', 0))
#         south = float(request.GET.get('south', 0))
#         east = float(request.GET.get('east', 0))
#         west = float(request.GET.get('west', 0))

#         # فیلتر کردن مشاغل و POIها بر اساس محدوده جغرافیایی
#         jobs = Job.objects.filter(
#             lat__gte=south, lat__lte=north, lng__gte=west, lng__lte=east
#         ).values('store_name', 'lat', 'lng', 'address', 'id')

#         pois = POI.objects.filter(
#             lat__gte=south, lat__lte=north, lng__gte=west, lng__lte=east
#         ).values('name', 'lat', 'lng', 'description', 'category')

#         return Response({
#             "jobs": list(jobs),
#             "pois": list(pois)
#         })
    




def provinces_cities_api(request):
    provinces = Province.objects.all().prefetch_related('counties__cities')

    data = []
    for province in provinces:
        province_data = {
            "id": province.id,
            "name": province.name,
            "lat": province.coordinates.y if province.coordinates else None,
            "lng": province.coordinates.x if province.coordinates else None,
            "counties": []
        }
        for county in province.counties.all():
            county_data = {
                "id": county.id,
                "name": county.name,
                "lat": county.coordinates.y if county.coordinates else None,
                "lng": county.coordinates.x if county.coordinates else None,
                "cities": []
            }
            for city in City.objects.filter(county__province=province):
                city_data = {
                    "id": city.id,
                    "name": city.name,
                    "lat": city.coordinates.y if city.coordinates else None,
                    "lng": city.coordinates.x if city.coordinates else None,
                }
                county_data["cities"].append(city_data)
            province_data["counties"].append(county_data)
        data.append(province_data)

    return JsonResponse(data, safe=False)



@login_required()
def map_view(request):
    return render(request, 'map/map.html')







@role_required('admin')
def make_seller(request, user_id):
    user_instance = get_object_or_404(user, id=user_id)
    job_form = JobForm()
    job_hours_form = JobHoursForm()
    time_slot_form = TimeSlotForm()
    days = JobHours.DAYS_OF_WEEK
    
    context = {
        'shifts': [1, 2, 3],
        'days':days,
        'job_form': job_form,
        'job_hours_form': job_hours_form,
        'time_slot_form': time_slot_form,
        'user': user_instance,  # Pass the user instance to the template
    }
    return render(request, 'admin_user/make_user_seller.html', context)




@role_required('admin')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.province_id = form.cleaned_data['province'].id if form.cleaned_data.get('province') else None
            user.city_id = form.cleaned_data['city'].id if form.cleaned_data.get('city') else None
            user.county_id = form.cleaned_data['city'].county_id if form.cleaned_data.get('city') else None  # فرض بر این که شهر دارای شهرستان است
            user.district_id = form.cleaned_data['district'].id if form.cleaned_data.get('district') else None  # ذخیره منطقه
            user.save()
            return redirect('user_list')  # تغییر به مسیر مناسب
    else:
        form = UserForm()
        roles = role.objects.all()
        provinces = Province.objects.all()
    return render(request, 'admin_user/add_user.html', {'form': form, 'provinces':provinces,'roles':roles})






from django.http import JsonResponse
from django.core.serializers import serialize
from .models import Province, County, City, Village, District

def load_counties(request):
    provinces = Province.objects.all()
    provinces_data = []

    for province in provinces:
        counties = County.objects.filter(province=province)
        counties_data = []

        for county in counties:
            cities = City.objects.filter(county=county)
            villages = Village.objects.filter(county=county)
            districts = District.objects.filter(county=county).order_by('id')  # اضافه کردن مناطق
            
            county_data = {
                "id": county.id,
                "name": county.name,
                "lat": county.coordinates.y if county.coordinates else None,
                "lng": county.coordinates.x if county.coordinates else None,
                "cities": [
                    {
                        "id": city.id,
                        "name": city.name,
                        "lat": city.coordinates.y if city.coordinates else None,
                        "lng": city.coordinates.x if city.coordinates else None,
                    }
                    for city in cities
                ],
                "villages": [
                    {
                        "id": village.id,
                        "name": village.name,
                        "lat": village.coordinates.y if village.coordinates else None,
                        "lng": village.coordinates.x if village.coordinates else None,
                    }
                    for village in villages
                ],
                "districts": [
                    {
                        "id": district.id,
                        "name": district.name,
                        "geometry": district.geometry.geojson if district.geometry else None,  # هندسه به فرمت GeoJSON
                    }
                    for district in districts
                ],
            }

            counties_data.append(county_data)

        provinces_data.append({
            "id": province.id,
            "name": province.name,
            "counties": counties_data,
        })

    return JsonResponse(provinces_data, safe=False)




class AddUserAPIView(APIView):
    
    def post(self, request):
        print('Received data:', request.data)  # بررسی داده‌های دریافتی
        data = request.data.copy()
        data['created_by_admin'] = True  # تنظیم فیلد created_by_admin
        
        # بررسی و افزودن district_id
        if 'district_id' in data:
            data['district_id'] = data['district_id']

        # تنظیم مختصات در صورت وجود
        if 'lat' in data and 'lng' in data:
            data['coordinates'] = {
                "type": "Point",
                "coordinates": [
                    float(data['lng']),
                    float(data['lat'])
                ]
            }

        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            new_user = serializer.save()
            return Response({
                'success': True,
                'message': 'کاربر با موفقیت ثبت شد!',
                'data': serializer.data,
                'user_id':new_user.id
            }, status=status.HTTP_201_CREATED)
        else:
            print('Serializer errors:', serializer.errors)  # بررسی خطاهای Serializer
            return Response({
                'success': False,
                'message': 'خطا در ثبت کاربر!',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)




class AddCategoryAPIView(APIView):
    
    parser_classes = [MultiPartParser, FormParser]  # افزودن پشتیبانی از آپلود فایل

    def post(self, request):
        serializer = CategoryJobsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'id': serializer.instance.id,  # شناسه دسته‌بندی ایجاد شده
                'message': 'دسته‌بندی با موفقیت اضافه شد.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'خطا در اعتبارسنجی داده‌ها',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


@role_required('admin')
def edit_category(request, category_id):
    category = get_object_or_404(category_job, id=category_id)
    all_categories = category_job.objects.exclude(id=category_id)
    hierarchical_categories = get_categories_hierarchically(all_categories)
    if request.method == 'POST':
        # دریافت داده‌ها از فرم
        category.name = request.POST.get('name')
        category.slug = request.POST.get('slug')
        category.label = request.POST.get('label')
        category.meta_keywords = request.POST.get('meta_keywords')
        category.meta_description = request.POST.get('meta_description')
        category.parent_id = request.POST.get('parent') or None
        category.has_slider = 'has_slider' in request.POST
        category.sort_order = request.POST.get('sort_order')
        category.status = request.POST.get('status') == 'true'

        # مدیریت تصاویر
        if request.POST.get('delete_icon') == 'true':
            if category.icon:
                category.icon.delete(save=False)
            category.icon = None

        if request.POST.get('delete_image') == 'true':
            if category.image:
                category.image.delete(save=False)
            category.image = None

        if request.POST.get('delete_banner') == 'true':
            if category.banner:
                category.banner.delete(save=False)
            category.banner = None

        # مدیریت فایل‌های جدید
        if 'icon' in request.FILES:
            category.icon = request.FILES['icon']
        if 'image' in request.FILES:
            category.image = request.FILES['image']
        if 'banner' in request.FILES:
            category.banner = request.FILES['banner']

        # ذخیره تغییرات
        category.save()
        return redirect('list_categories')
    
    
    return render(request, 'admin_user/edit_category.html', {
        'category': category,
        'categories': hierarchical_categories
    })





    


class AddJobAPIView(APIView):
    
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'id': serializer.instance.id,
                'message': 'فروشنده با موفقیت اضافه شد.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': 'خطا در اعتبارسنجی داده‌ها',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    


def add_job(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # ذخیره کاربر با فیلدهای استان و شهر
            user = form.save(commit=False)
            user.province_id = form.cleaned_data['province'].id
            user.city_id = form.cleaned_data['city'].id
            user.county_id = form.cleaned_data['county'].id

            user.save()
            user_id = user.id
            return redirect(f'create-job/{user_id}/')  # تغییر به مسیر مناسب
    else:
        title = "ایجاد شغل - مرحله اول"
        form = UserForm()
        roles = role.objects.all()
        provinces = Province.objects.all()
    return render(request, 'admin_user/add_seller.html', {'form': form, 'provinces':provinces,'roles':roles, 'title':title})


@login_required
def edit_user_view(request, user_id):
    user_instance = get_object_or_404(user, id=user_id)  # This is your target user
    roles = role.objects.all()
    provinces = Province.objects.all()
    city = get_object_or_404(City, id=user_instance.city_id)
    cities = City.objects.all()
    user_province = get_object_or_404(Province, id=user_instance.province_id)

    # Fix: Use user_instance instead of user
    if user_instance.coordinates:  # ← This is the critical change
        user_lat = user_instance.coordinates.y  # Latitude
        user_lng = user_instance.coordinates.x  # Longitude
    else:
        user_lat = None
        user_lng = None

    print(f"user lat is {user_lat}")
    print(f"user lng is {user_lng}")

    return render(request, 'admin_user/edit_user.html', {
        'provinces': provinces,
        'cities': cities,
        'usercity': city,
        'user_lat': user_lat,
        'user_lng': user_lng,
        'user_province': user_province,
        'user': user_instance,
        'roles': roles,
        'current_role': role_user.objects.filter(user=user_id).first().role.display_name
    })



class EditUserAPIView(APIView):
    
    def put(self, request, user_id):
        user_instance = get_object_or_404(user, id=user_id)
        serializer = UserSerializer(user_instance, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'کاربر با موفقیت ویرایش شد!',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': 'خطا در ویرایش کاربر!',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        user_instance = get_object_or_404(user, id=user_id)
        

        return Response({
            'user': UserSerializer(user_instance).data,
        })
    







def provinces_cities_api(request):
    provinces = Province.objects.prefetch_related('counties__cities', 'counties__districts')

    data = []
    for province in provinces:
        province_data = {
            "id": province.id,
            "name": province.name,
            "lat": province.coordinates.y if province.coordinates else None,
            "lng": province.coordinates.x if province.coordinates else None,
            "counties": []
        }

        for county in province.counties.all():
            county_data = {
                "id": county.id,
                "name": county.name,
                "lat": county.coordinates.y if county.coordinates else None,
                "lng": county.coordinates.x if county.coordinates else None,
                "cities": [],
                "districts": []  # افزودن مناطق شهری
            }

            # افزودن مناطق شهری شهرستان
            for district in county.districts.all():
                district_data = {
                    "id": district.id,
                    "name": district.name,
                    "polygon": district.geometry.geojson  # هندسه به فرمت GeoJSON
                }
                county_data["districts"].append(district_data)

            for city in county.cities.all():
                city_data = {
                    "id": city.id,
                    "name": city.name,
                    "lat": city.coordinates.y if city.coordinates else None,
                    "lng": city.coordinates.x if city.coordinates else None,
                }
                county_data["cities"].append(city_data)

            province_data["counties"].append(county_data)

        data.append(province_data)

    return JsonResponse(data, safe=False)






def main_view(request):
    return render(request, 'main/main.html')



def logout_view(request):
    logout(request)
    return redirect('login')







@api_view(['POST'])
@csrf_exempt 
def create_job(request):
    if request.method == 'POST':
        print("Request data:", request.data)  # Log incoming data
        # ساخت شغل جدید
        job_serializer = JobSerializer(data=request.data)
        if job_serializer.is_valid():
            new_job = job_serializer.save()

            # تغییر نقش کاربر به seller
            job_user = new_job.user  # کاربر جاری
            seller_role = get_object_or_404(role, name='seller')  # یافتن نقش seller

            # بررسی آیا کاربر قبلاً نقش seller داشته است یا نه
            role_user_instance, created = role_user.objects.get_or_create(
                user=job_user,
                defaults={'role': seller_role}
            )

            # اگر نقش کاربر قبلاً seller نبوده، آن را به seller تغییر دهید
            if not created and role_user_instance.role != seller_role:
                role_user_instance.role = seller_role
                role_user_instance.save()

            return Response({'id': new_job.id}, status=status.HTTP_201_CREATED)
        return Response(job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@csrf_exempt
def create_job_hours(request, job_id):
    try:
        thejob = job.objects.get(id=job_id)
    except thejob.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)

    day = request.data.get('day')
    shifts = request.data.get('shifts', [])
    
    # ایجاد یا دریافت JobHour موجود
    job_hour, _ = JobHours.objects.get_or_create(job=thejob, day=day)
    
    # پردازش شیفت‌ها
    for shift in shifts:
        start = shift.get('start')
        end = shift.get('end')
        if not start or not end:
            continue  # نادیده گرفتن شیفت‌های ناقص
        
        try:
            # ایجاد شیفت فقط اگر وجود نداشته باشد
            TimeSlot.objects.create(
                job_hour=job_hour,
                start_time=start,
                end_time=end
            )
        except IntegrityError:
            # اگر شیفت تکراری بود، ادامه دهید
            continue
    
    return Response({'status': 'success'}, status=200)




@api_view(['POST'])
@csrf_exempt
def create_job_links(request, job_id):
    try:
        thejob = job.objects.get(id=job_id)
    except thejob.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)

    serializer = JobLinksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(job=thejob)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)




@role_required('admin')
def settings_view(request):
    # شرط‌های فیلتر کردن
    settings = setting.objects.all().order_by('id')

    return render(request, 'admin_user/setting.html', {'settings': settings})




@role_required('admin')
def update_category_status(request, pk):
    if request.method == 'PATCH':
        try:
            category = category_job.objects.get(pk=pk)
        except category_job.DoesNotExist:
            return JsonResponse({"error": "دسته‌بندی یافت نشد"}, status=404)

        # تغییر وضعیت
        category.status = not category.status
        category.save()

        return JsonResponse({"message": "وضعیت دسته‌بندی با موفقیت به‌روزرسانی شد", "status": category.status}, status=200)
    else:
        return JsonResponse({"error": "متد درخواست معتبر نیست"}, status=405)
    


@role_required('admin')
@csrf_exempt
def edit_setting_ajax(request):
    if request.method == 'POST':
        setting_id = request.POST.get('setting_id')
        new_value = request.POST.get('value')
        try:
            setting_instance = setting.objects.get(id=setting_id)
            setting_instance.value = new_value
            setting_instance.save()
            return JsonResponse({'success': True})
        except setting.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'رکورد پیدا نشد'})
    return JsonResponse({'success': False, 'error': 'درخواست نامعتبر'})




class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.prefetch_related('job_set').all()  # پیش‌بارگذاری Jobهای مرتبط
    serializer_class = PlaceSerializer

class IndependentJobViewSet(viewsets.ModelViewSet):
    queryset = job.objects.filter(place__isnull=True, coordinates__isnull=False)  # فقط Jobهایی که Place ندارند
    serializer_class = JobSerializer




class CategoryJobView(APIView):
    def get(self, request):
        # محاسبه تعداد job‌ها برای هر دسته‌بندی
        categories = category_job.objects.filter(parent__isnull=True).annotate(
            job_count=Count('category_place__job', distinct=True)
        )
        serializer = CategoryJobSerializer(categories, many=True)
        return Response({"categories": serializer.data})




class ProvinceView(APIView):
    def get(self, request):
        # محاسبه تعداد job‌ها برای استان‌ها
        provinces = Province.objects.annotate(job_count=Count('counties__cities__job'))
        
        # محاسبه تعداد job‌ها برای شهرستان‌ها
        counties = County.objects.annotate(job_count=Count('cities__job'))
        
        # محاسبه تعداد job‌ها برای شهرها
        cities = City.objects.annotate(job_count=Count('job'))
        
        # محاسبه تعداد job‌ها برای مناطق
        districts = District.objects.annotate(job_count=Count('job'))

        # محاسبه تعداد job‌ها برای روستاها
        villages = Village.objects.annotate(job_count=Count('job'))

        # سریالایز کردن داده‌ها
        province_serializer = ProvinceSerializer(provinces, many=True)
        county_serializer = CountySerializer(counties, many=True)
        city_serializer = CitySerializer(cities, many=True)
        district_serializer = DistrictSerializer(districts, many=True)
        village_serializer = VillageSerializer(villages, many=True)

        # ترکیب پاسخ‌ها
        response_data = {
            "provinces": province_serializer.data,
            "counties": county_serializer.data,
            "cities": city_serializer.data,
            "districts": district_serializer.data,
            "villages": village_serializer.data,
        }

        return Response(response_data)
    




@api_view(['GET'])
def get_independent_jobs_and_commercial_places(request):
    logger.debug("Starting get_independent_jobs_and_commercial_places")
    
    # دریافت پارامترهای فیلتر
    province_id = request.query_params.get('province')
    county_id = request.query_params.get('county')
    city_id = request.query_params.get('city')
    category_id = request.query_params.get('category')
    min_lat = request.query_params.get('min_lat')  # حداقل عرض جغرافیایی
    max_lat = request.query_params.get('max_lat')  # حداکثر عرض جغرافیایی
    min_lng = request.query_params.get('min_lng')  # حداقل طول جغرافیایی
    max_lng = request.query_params.get('max_lng')  # حداکثر طول جغرافیایی
    page = int(request.query_params.get('page', 1))  # شماره صفحه (پیش‌فرض: 1)
    page_size = int(request.query_params.get('page_size', 30))  # تعداد نتایج در هر صفحه (پیش‌فرض: 30)

    # فیلتر کردن مشاغل
    independent_jobs = Job.objects.filter(place__isnull=True, coordinates__isnull=False)  # مشاغل مستقل
    commercial_places = Place.objects.all()  # همه مکان‌ها

    # اعمال فیلترها روی مشاغل مستقل
    if province_id:
        independent_jobs = independent_jobs.filter(province_id=province_id)
    if county_id:
        independent_jobs = independent_jobs.filter(county_id=county_id)
    if city_id:
        independent_jobs = independent_jobs.filter(city_id=city_id)
    if category_id:
        independent_jobs = independent_jobs.filter(category_place__category_id=category_id)
    if min_lat and max_lat and min_lng and max_lng:  # فیلتر بر اساس محدوده جغرافیایی
        try:
            min_lat = float(min_lat)
            max_lat = float(max_lat)
            min_lng = float(min_lng)
            max_lng = float(max_lng)
            independent_jobs = independent_jobs.filter(
                latitude__gte=min_lat,
                latitude__lte=max_lat,
                longitude__gte=min_lng,
                longitude__lte=max_lng
            )
        except ValueError:
            return Response({"error": "Invalid latitude or longitude values."}, status=400)

    # اعمال فیلترها روی مکان‌ها
    if province_id:
        commercial_places = commercial_places.filter(province_id=province_id)
    if county_id:
        commercial_places = commercial_places.filter(county_id=county_id)
    if city_id:
        commercial_places = commercial_places.filter(city_id=city_id)
    if category_id:
        # فیلتر مکان‌ها بر اساس دسته‌بندی مشاغل
        commercial_places = commercial_places.filter(jobs__category_place__category_id=category_id).distinct()
    if min_lat and max_lat and min_lng and max_lng:  # فیلتر بر اساس محدوده جغرافیایی
        try:
            min_lat = float(min_lat)
            max_lat = float(max_lat)
            min_lng = float(min_lng)
            max_lng = float(max_lng)
            commercial_places = commercial_places.filter(
                latitude__gte=min_lat,
                latitude__lte=max_lat,
                longitude__gte=min_lng,
                longitude__lte=max_lng
            )
        except ValueError:
            return Response({"error": "Invalid latitude or longitude values."}, status=400)

    # صفحه‌بندی نتایج
    paginator_jobs = Paginator(independent_jobs, page_size)
    paginator_places = Paginator(commercial_places, page_size)

    # دریافت نتایج صفحه فعلی
    try:
        jobs_page = paginator_jobs.page(page)
        places_page = paginator_places.page(page)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    # سریالایز کردن داده‌ها
    job_serializer = JobSerializer(jobs_page.object_list, many=True)
    place_serializer = PlaceSerializer(places_page.object_list, many=True)

    # برگرداندن پاسخ
    return Response({
        "independent_jobs_count": paginator_jobs.count,
        "commercial_places_count": paginator_places.count,
        "current_page": page,
        "total_pages": max(paginator_jobs.num_pages, paginator_places.num_pages),
        "independent_jobs": job_serializer.data,
        "commercial_places": place_serializer.data
    })



class JobDetailAPIView(APIView):

    def get(self, request, id):
        try:
            # پیدا کردن شغل بر اساس id
            thejob = job.objects.get(id=id)
            serializer = JobSerializerForFlutter(thejob)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except job.DoesNotExist:
            return Response(
                {"status": "error", "message": "شغل مورد نظر یافت نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": "خطای سرور رخ داده است."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




