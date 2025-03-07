from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.contrib.gis.db import models as gis_models
from django.db.models import Index
import uuid
from django.utils.translation import gettext_lazy as _


class Province(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    coordinates = gis_models.PointField()  # ذخیره مختصات جغرافیایی به عنوان نقطه

    class Meta:
        db_table = 'provinces'
        verbose_name = "استان"
        verbose_name_plural = "استان ها"
        indexes = [  # تعریف شاخص GIST
            Index(fields=['coordinates'], name='province_coordinates_idx')
        ]

    def __str__(self):
        return self.name
    


class County(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="counties")
    
    coordinates = gis_models.PointField(null=True, blank=True)

    class Meta:
        db_table = 'counties'
        verbose_name = "شهرستان "
        verbose_name_plural = "شهرستان ها"
        indexes = [
            Index(fields=['coordinates'], name='county_coordinates_idx')
        ]

    def __str__(self):
        return self.name
    


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="cities")
    coordinates = gis_models.PointField(null=True, blank=True)

    class Meta:
        db_table = 'cities'
        verbose_name = "شهر"
        verbose_name_plural = "شهر ها"
        indexes = [
            Index(fields=['coordinates'], name='city_coordinates_idx')
        ]

    def __str__(self):
        return self.name



class Village(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="villages")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="villages")
    coordinates = gis_models.PointField(null=True, blank=True)

    class Meta:
        db_table = 'villages'
        verbose_name = "روستا"
        verbose_name_plural = "روستا ها"
        indexes = [
            Index(fields=['coordinates'], name='village_coordinates_idx')
        ]
        

    def __str__(self):
        return self.name




















class District(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام منطقه")
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='districts', verbose_name="شهرستان")
    geometry = gis_models.PolygonField(verbose_name="هندسه")

    class Meta:
        db_table = 'districts'
        indexes = [
            Index(fields=['geometry'], name='district_coordinates_idx')
        ]
        verbose_name = "منطقه"
        verbose_name_plural = "مناطق"
        ordering = ['name']


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
    county_id = models.IntegerField(null=True, blank=True)
    city_id = models.IntegerField(null=True, blank=True)
    village_id = models.IntegerField(null=True, blank=True)
    district_id = models.IntegerField(null=True, blank=True)
    coordinates = gis_models.PointField(
        srid=4326,  # سیستم مختصات WGS 84
        null=True,
        blank=True,
        verbose_name='مختصات'
    )
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
    is_mobile_confirmed = models.BooleanField()
    created_by_admin = models.BooleanField(default=False)

    
    class Meta:
        db_table = 'users'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['id']

    def __str__(self):
        return self.username


# دسته‌بندی ها
class category_job(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    icon = models.ImageField(upload_to='media/categories/icons/', null=True, blank=True)
    image = models.ImageField(upload_to='media/categories/images/', null=True, blank=True)
    banner = models.ImageField(upload_to='media/categories/banners/', null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    has_slider = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    view_counts = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'category_job'
        verbose_name = 'دسته‌بندی مشاغل'
        verbose_name_plural = 'دسته‌بندی مشاغل'
        ordering = ['sort_order']
        get_latest_by = 'created_at'
        get_latest_by = 'updated_at'


    def __str__(self):
        return self.name






# نقش‌ها
class role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'roles'
        verbose_name = 'نقش'
        verbose_name_plural = 'نقش‌ها'
        ordering = ['name']


    def __str__(self):
        return self.display_name


# نقش کاربران
class role_user(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    role = models.ForeignKey(role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def generate_job_code():
    return str(uuid.uuid4().int)[:10]




class Place(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    coordinates = gis_models.PointField(
        srid=4326,
        null=True,
        blank=True,
        verbose_name='مختصات'
    )
    address = models.TextField()
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='places')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'place'
        verbose_name = 'مکان'
        verbose_name_plural = 'مکان‌ها'
        ordering = ['name']

    def __str__(self):
        return self.name
    

# مشاغل
class job(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    job_code = models.CharField(max_length=10, unique=True, default=generate_job_code)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True,)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True,)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True,)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField()
    post_code = models.CharField(max_length=20, null=True, blank=True)
    # lat = models.DecimalField(max_digits=9, decimal_places=6)
    # lng = models.DecimalField(max_digits=9, decimal_places=6)
    coordinates = gis_models.PointField(
        srid=4326,  # سیستم مختصات WGS 84
        null=True,
        blank=True,
        verbose_name='مختصات'
    )


    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='مکان تجاری', related_name='jobs')


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


    class Meta:
        db_table = 'jobs'
        verbose_name = 'کار'
        verbose_name_plural = 'کارها'
        ordering = ['-created_at']

    def __str__(self):
        return self.store_name
    
    def coordinates_display(self):
        if self.coordinates:
            return f"طول: {self.coordinates.x:.6f}, عرض: {self.coordinates.y:.6f}"
        return "تعیین نشده"
    
    def get_nearby_pois(self, radius_km=5):
        if not self.coordinates:
            return Place.objects.none()

        point = self.coordinates
        return Place.objects.filter(coordinates__distance_lte=(point, D(km=radius_km)))
    

    coordinates_display.short_description = "مختصات"

    

# دسته‌بندی  مشاغل
class category_place(models.Model):
    category = models.ForeignKey(category_job, on_delete=models.CASCADE)
    job = models.ForeignKey(job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category_place'


# تنظیمات
class setting(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'settings'
    
    def __str__(self):
        return self.label



class JobHours(models.Model):
    DAYS_OF_WEEK = [
        ('sat', _('شنبه')),
        ('sun', _('یکشنبه')),
        ('mon', _('دوشنبه')),
        ('tue', _('سه‌شنبه')),
        ('wed', _('چهارشنبه')),
        ('thu', _('پنجشنبه')),
        ('fri', _('جمعه')),
    ]
    
    job = models.ForeignKey(job, on_delete=models.CASCADE, verbose_name=_("کسب‌وکار"))
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK, verbose_name=_("روز هفته"))
    is_closed = models.BooleanField(default=False, verbose_name=_("تعطیل"))
    
    class Meta:
        db_table = 'job_hours'
        verbose_name = _('ساعت کاری')
        verbose_name_plural = _('ساعت‌های کاری')
        unique_together = ('job', 'day')  # هر روز برای یک کسب‌وکار فقط یک بار ثبت شود
    
    def __str__(self):
        return f"{self.get_day_display()} - {self.job}"
    

    
class TimeSlot(models.Model):
    job_hour = models.ForeignKey(JobHours, on_delete=models.CASCADE, related_name='time_slots', verbose_name=_("ساعت کاری"))
    start_time = models.TimeField(verbose_name=_("زمان شروع"))
    end_time = models.TimeField(verbose_name=_("زمان پایان"))
    
    class Meta:
        db_table = 'time_slots'
        verbose_name = _('بازه زمانی')
        verbose_name_plural = _('بازه‌های زمانی')
        constraints = [
            models.UniqueConstraint(
                fields=['job_hour', 'start_time', 'end_time'],
                name='unique_time_slot'
            )
        ]
    
    def __str__(self):
        return f"{self.start_time} - {self.end_time}"
    




class JobLinks(models.Model):
    job = models.ForeignKey(job, on_delete=models.CASCADE)
    website = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    robika = models.URLField(null=True, blank=True)
    eitaa = models.URLField(null=True, blank=True)
    bale = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'job_links'
        verbose_name = _('لینک شغل ')
        verbose_name_plural = _('لینک های شغل')

    def __str__(self):
        return f"Links for {self.job}"
