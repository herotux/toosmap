from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import user, role_user, category_jobs, Province, City, job, role
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
from .forms import UserForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, CategoryJobsSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q




def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.is_superuser or role_user.objects.filter(user=request.user, role__name=role).exists():
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator

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
        mobile_number = request.POST['mobile_number']
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

    return render(request, 'registration/login.html')

def verify_password(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        user_instance = user.objects.filter(username=mobile_number).first()

        if user_instance and user_instance.check_password(password):
            login(request, user_instance)
            return redirect('user_dashboard')  # Redirect to home page
        else:
            return render(request, 'registration/login_password.html', {'mobile_number': mobile_number, 'error': 'Invalid password.'})

    return render(request, 'registration/login_password.html')

def otp_login(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        otp = request.session.get('otp')
        if otp and request.POST['otp'] == str(otp):
            user_instance = user.objects.get(username=mobile_number)
            login(request, user_instance)
            return redirect('home')  # Redirect to home page
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
            return redirect('home')  # Redirect to home page
        else:
            return render(request, 'registration/verify_otp.html', {'error': 'Invalid OTP.'})
    return render(request, 'registration/verify_otp.html')

# Dashboard views
@role_required('admin')
@login_required
def admin_dashboard(request):
    user_info = {
        'name': request.user.username,
        'role': role_user.objects.filter(user=request.user).first().role.display_name
    }
    return render(request, 'admin/dashboard.html', {'user_info': user_info})

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
    return render(request, 'home.html', {'user_info': user_info})

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

    return render(request, 'admin/users_list.html', {'page_obj': page_obj, 'user_roles': user_roles})




def list_categories(request):
    # دریافت مقدار records_per_page از پارامتر GET
    records_per_page = request.GET.get('records_per_page', '')

    # اگر مقدار خالی یا نامعتبر بود، از مقدار پیش‌فرض استفاده کنید
    try:
        records_per_page = int(records_per_page)
    except ValueError:
        records_per_page = 10  # مقدار پیش‌فرض

    # دریافت دسته‌های والد و مرتب‌سازی بر اساس sort_order
    categories = category_jobs.objects.filter(parent=None).order_by('sort_order')

    # ایجاد Paginator
    paginator = Paginator(categories, records_per_page)

    # دریافت شماره صفحه از پارامتر GET
    page_number = request.GET.get('page')

    # دریافت صفحه مورد نظر
    page_obj = paginator.get_page(page_number)

    # افزودن زیرمجموعه‌ها به هر دسته‌بندی والد
    for category in page_obj:
        category.subcategories = category_jobs.objects.filter(parent=category).order_by('sort_order')

    return render(request, 'admin/categories.html', {'page_obj': page_obj})



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
    
def add_category(request):
    categories = category_jobs.objects.filter(parent=None).order_by('sort_order')
    return render(request, 'admin/add_category.html',{'categories': categories})

def edit_category(request, category_id):
    category = get_object_or_404(category_jobs, id=category_id)
    if request.method == 'POST':
        category.name = request.POST['name']
        category.slug = request.POST['slug']
        category.save()
        return redirect('list_categories')
    return render(request, 'admin/edit_category.html', {'category': category})

def delete_category(request, category_id):
    category = get_object_or_404(category_jobs, id=category_id)
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
    





class ProvinceCityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # اصلاح نام مدل به صورت صحیح
        provinces = Province.objects.all()
        
        # ساخت داده برای ارسال به فرانت‌اند
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




@csrf_exempt  # غیرفعال کردن CSRF برای سادگی (در محیط تولید از روش‌های امن‌تر استفاده کنید)
@user_passes_test(lambda u: u.is_superuser)  # فقط ادمین‌ها می‌توانند نقش کاربر را تغییر دهند
def make_seller_api(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(user, id=user_id)
        seller_role = role.objects.get(name='seller')  # فرض کنید نقش فروشنده با نام 'فروشنده' وجود دارد
        
        # اگر کاربر نقش فروشنده ندارد، آن را اضافه کنید
        if seller_role not in user.roles.all():
            user.roles.add(seller_role)
            return JsonResponse({'status': 'success', 'message': 'نقش کاربر به فروشنده تغییر یافت.'})
        else:
            return JsonResponse({'status': 'warning', 'message': 'این کاربر قبلاً فروشنده است.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'درخواست نامعتبر است.'}, status=400)





def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # ذخیره کاربر با فیلدهای استان و شهر
            user = form.save(commit=False)
            user.province_id = form.cleaned_data['province'].id
            user.city_id = form.cleaned_data['city'].id
            user.save()
            return redirect('user_list')  # تغییر به مسیر مناسب
    else:
        form = UserForm()
    return render(request, 'admin/add_user.html', {'form': form})






def load_cities(request):
    provinces = Province.objects.all()
    provinces_data = []
    for province in provinces:
        cities = City.objects.filter(province=province)
        cities_data = [{"name": city.name, "lat": city.lat, "lng": city.lng} for city in cities]
        provinces_data.append({
            "name": province.name,
            "cities": cities_data
        })
    return JsonResponse(provinces_data, safe=False)





class AddUserAPIView(APIView):
    def post(self, request):
        print('Received data:', request.data)  # بررسی داده‌های دریافتی
        data = request.data.copy()
        data['created_by_admin'] = True  # تنظیم فیلد created_by_admin
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'کاربر با موفقیت ثبت شد!',
                'data': serializer.data
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

    return render(request, 'admin/add_seller.html')


@login_required
def edit_user_view(request, user_id):
    user_instance = get_object_or_404(user, id=user_id)
    roles = role.objects.all()  # Fetch all roles
    provinces = Province.objects.all()
    city = get_object_or_404(City, id=user_instance.city_id)
    cities = City.objects.all()
    user_province = get_object_or_404(Province, id=user_instance.province_id)
    return render(request, 'admin/edit_user.html', {
        'provinces': provinces,
        'cities':cities,
        'usercity':city,
        'user_province':user_province,
        'user': user_instance,
        'roles': roles, # Pass roles to the template
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