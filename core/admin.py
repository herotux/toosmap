from django.contrib import admin
from .models import TimeSlot, County, District, Village, setting, user, role_user, job, category_place, role, category_job, Province, City, role, role_user, JobHours, JobLinks
from django.contrib.gis.admin import GISModelAdmin
from leaflet.admin import LeafletGeoAdmin
from django.utils.safestring import mark_safe


class JobAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'map_preview')
    
    def map_preview(self, obj):
        if obj.coordinates:
            return mark_safe(
                f'<a href="https://www.openstreetmap.org/?mlat={obj.coordinates.y}&mlon={obj.coordinates.x}" target="_blank">مشاهده روی نقشه</a>'
            )
        return "بدون موقعیت"
    
    map_preview.short_description = "پیش نمایش"


admin.site.register(job, JobAdmin)

# Register your models here.
admin.site.register(user)
admin.site.register(category_place)
admin.site.register(role)
admin.site.register(role_user)
admin.site.register(category_job)  
admin.site.register(Province)
admin.site.register(City) 
admin.site.register(JobHours)  
admin.site.register(JobLinks)  
admin.site.register(setting)
admin.site.register(District)
admin.site.register(Village)
admin.site.register(County)
admin.site.register(TimeSlot)
