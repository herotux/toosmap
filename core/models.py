from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.contrib.gis.db import models


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'province'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, related_name='cities', on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        db_table = 'city'

    def __str__(self):
        return self.name




class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام منطقه")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts', verbose_name="شهر")
    geometry = models.PolygonField(verbose_name="هندسه")

    def __str__(self):
        return self.name



class Village(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام روستا")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='villages', verbose_name="شهر")
    geometry = models.PolygonField(verbose_name="هندسه")

    def __str__(self):
        return self.name
    
    

# کاربران
class user(AbstractUser):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    user_code = models.CharField(max_length=10, unique=True, default=str(random.randint(1000000000, 9999999999)))
    mobile = models.CharField(max_length=15, unique=True)
    national_code = models.CharField(max_length=10, null=True, blank=True)
    national = models.BooleanField(default=False)
    province_id = models.IntegerField(null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=128)
    remember_token = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    wallets = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    last_active = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_mobile_confirmed = models.BooleanField(default=False)  # New field for mobile confirmation
    created_by_admin = models.BooleanField(default=False)
    lat = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    lng = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    
    
    def __str__(self):
        return self.username


# دسته‌بندی مشاغل
class category_jobs(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    icon = models.ImageField(upload_to='categories/icons/', null=True, blank=True)
    image = models.ImageField(upload_to='categories/images/', null=True, blank=True)
    banner = models.ImageField(upload_to='categories/banners/', null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    has_slider = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    view_counts = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# دسته‌بندی کاربران مشاغل
class category_user(models.Model):
    category = models.ForeignKey(category_jobs, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# نقش‌ها
class role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name


# نقش کاربران
class role_user(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# مشاغل
class job(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    job_code = models.CharField(max_length=10, unique=True, default=str(random.randint(1000000000, 9999999999)))
    mobile = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    post_code = models.CharField(max_length=20, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    in_person = models.BooleanField(default=False)
    internet_sales = models.BooleanField(default=False)
    single_sale = models.BooleanField(default=False)
    wholesale_sales = models.BooleanField(default=False)
    is_producer = models.BooleanField(default=False)
    unused_product = models.BooleanField(default=False)
    used_product = models.BooleanField(default=False)
    buyer = models.BooleanField(default=False)
    purchase_in_store = models.BooleanField(default=False)
    purchase_in_home = models.BooleanField(default=False)
    slang = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    profile = models.ImageField(upload_to='jobs/profiles/', null=True, blank=True)
    last_active = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# تنظیمات
class setting(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label


class Locality(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class JobHours(models.Model):
    job = models.ForeignKey(job, on_delete=models.CASCADE)
    saturday = models.TimeField()
    sunday = models.TimeField()
    monday = models.TimeField()
    tuesday = models.TimeField()
    wednesday = models.TimeField()
    thursday = models.TimeField()
    friday = models.TimeField()

    def __str__(self):
        return f"Hours for {self.job}"


class JobLinks(models.Model):
    job = models.ForeignKey(job, on_delete=models.CASCADE)
    website = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    robika = models.URLField(null=True, blank=True)
    eitaa = models.URLField(null=True, blank=True)
    bale = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Links for {self.job}"
