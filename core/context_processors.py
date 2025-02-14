# yourapp/context_processors.py

from .models import user, role_user

def current_user(request):
    user_role = None
    if request.user.is_authenticated:
        role = role_user.objects.filter(user=request.user).first()
        user_role = role.role.display_name if role else None
    return {
        'current_user': request.user,
        'user_role': user_role,
    }