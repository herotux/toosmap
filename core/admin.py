from django.contrib import admin
from .models import setting, user, role_user, job, category_user, role, category_jobs, Province, City, category_user, role, role_user, Locality, JobHours, JobLinks

# Register your models here.
admin.site.register(user)
admin.site.register(job)
admin.site.register(category_user)
admin.site.register(role)
admin.site.register(role_user)
admin.site.register(category_jobs)  
admin.site.register(Province)
admin.site.register(City)
admin.site.register(Locality)  
admin.site.register(JobHours)  
admin.site.register(JobLinks)  
admin.site.register(setting)
