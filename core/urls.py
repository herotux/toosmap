from django.contrib import admin
from django.urls import path, include
from .views import AddCategoryAPIView, EditUserAPIView, AddUserAPIView, load_cities, list_users, register, otp_login, login_view, verify_otp, verify_password, map_view, admin_dashboard, seller_dashboard, user_dashboard, list_categories, add_category, edit_category, delete_category, ProvinceCityAPIView, add_user  # Import the add_user view
from .views import AddJobAPIView, add_job, edit_user_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('otp-login/', otp_login, name='otp_login'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('verify_password/', verify_password, name='verify_password'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    
    # Category management URLs
    path('admin/categories/', list_categories, name='list_categories'),
    path('admin/categories/add/', add_category, name='add_category'),
    path('admin/categories/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('admin/categories/delete/<int:category_id>/', delete_category, name='delete_category'),
    
    # User management URLs
    path('admin/users/', list_users, name='list_users'),
    path('admin/users/add/', add_user, name='add_user'),  # New URL for adding a user
    path('api/provinces-cities/', ProvinceCityAPIView.as_view(), name='provinces_cities'),
    path('map/', map_view, name='map'),
    path('load-cities/', load_cities, name='load_cities'),
    path('api/add-user/', AddUserAPIView.as_view(), name='add_user_api'),
    path('api/add-category/', AddCategoryAPIView.as_view(), name='add_category_api'),
    path('api/add-job/', AddJobAPIView.as_view(), name='add-job'),
    path('admin/seller/create/', add_job, name='add_seller'),
    path('api/edit-user/<int:user_id>/', EditUserAPIView.as_view(), name='edit_user'),
    path('admin/edit-user/<int:user_id>/', edit_user_view, name='edit_user_view'),
    
]
