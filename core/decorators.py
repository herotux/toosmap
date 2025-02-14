from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponseForbidden 
from django.urls import reverse
from .models import role_user

def role_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # بررسی اینکه کاربر وارد سیستم شده است
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login') + '?next=' + request.path)

            # بررسی اینکه کاربر ادمین است یا نقش مورد نظر را دارد
            if request.user.is_superuser or role_user.objects.filter(user=request.user, role__name=role).exists():
                return view_func(request, *args, **kwargs)

            # اگر کاربر مجوز نداشته باشد
            return HttpResponseForbidden("You do not have permission to access this page.")
        return _wrapped_view
    return decorator