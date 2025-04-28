from django.contrib import admin
from django.urls import path, include
from .views import edit_category,ProvinceListView, AddCategoryAPIView, EditUserAPIView, AddUserAPIView, load_counties, list_users, register, otp_login, login_view, verify_otp, verify_password, map_view, admin_dashboard, seller_dashboard, user_dashboard, list_categories, add_category, edit_category, delete_category, ProvinceCityAPIView, add_user  # Import the add_user view
from .views import LocationView, VersionSettingView, PlaceDetailAPIView, JobDetailAPIView, get_independent_jobs_and_commercial_places, ProvinceView, CategoryJobView, IndependentJobViewSet, PlaceViewSet, edit_setting_ajax, update_category_status, home, settings_view, create_job_hours, create_job_links, create_job, logout_view, AddJobAPIView, make_seller, add_job, edit_user_view, provinces_cities_api, main_view
from .views import test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17

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
    path('api/provinces-cities/', provinces_cities_api, name='provinces_cities'),
    path('map/', map_view, name='map'),
    path('load-counties/', load_counties, name='load_counties'),
    path('api/add-user/', AddUserAPIView.as_view(), name='add_user_api'),
    path('api/add-category/', AddCategoryAPIView.as_view(), name='add_category_api'),
    path(
        'api/categories/<int:category_id>/edit/',
        edit_category,
        name='edit_category_api'
    ),
    path('api/add-job/', AddJobAPIView.as_view(), name='add-job'),
    path('admin/seller/create/', add_job, name='add_seller'),
    path('api/edit-user/<int:user_id>/', EditUserAPIView.as_view(), name='edit_user'),
    path('admin/edit-user/<int:user_id>/', edit_user_view, name='edit_user_view'),
    path('main/', main_view, name='main'),
    path('create-job/<int:user_id>/', make_seller, name='make_seller'),
    path('logout/', logout_view, name='logout'),
    path('api/jobs/create/', create_job, name='create_job'),
    path('api/jobs/<int:job_id>/hours/', create_job_hours, name='create_job_hours'),
    path('api/jobs/<int:job_id>/links/', create_job_links, name='create_job_links'),
    path('', home, name='home'),
    path('admin/settings/', settings_view, name='settings'),
    path('admin/category/<int:pk>/update-status/', update_category_status, name='cat-job-update-status'),
    path('edit_setting_ajax/', edit_setting_ajax, name='edit_setting_ajax'),
    path('api/places/', PlaceViewSet.as_view({'get': 'list'}), name='places'),
    path('api/independent-jobs/', IndependentJobViewSet.as_view({'get': 'list'}), name='independent-jobs'),
    path('api/categories/', CategoryJobView.as_view(), name='categories'),
    path('api/provinces/', ProvinceListView.as_view(), name='provinces'),
    path('api/locations/', LocationView.as_view(), name='locations'),
    path('api/all_provinces/', ProvinceView.as_view(), name='provinces'),
    
    path('api/jobs-and-places/', get_independent_jobs_and_commercial_places, name='jobs-and-places'),
    path('api/jobs/<int:id>/', JobDetailAPIView.as_view(), name='job-detail'),
    path('api/places/<int:id>/', PlaceDetailAPIView.as_view(), name='place-detail'),
    path('api/version/', VersionSettingView.as_view(), name='version-setting'),
    
    path('test1/', test1, name='test1'),
    path('test2/', test2, name='test2'),
    path('test3/', test3, name='test3'),
    path('test4/', test4, name='test4'),
    path('test5/', test5, name='test5'),
    path('test6/', test6, name='test6'),
    path('test7/', test7, name='test7'),
    path('test8/', test8, name='test8'),

    path('test10/', test10, name='test10'),
    path('test11/', test11, name='test11'),
    path('test12/', test12, name='test12'),
    path('test13/', test13, name='test13'),
    path('test14/', test14, name='test14'),
    path('test15/', test15, name='test15'),
    path('test16/', test16, name='test16'),
    path('test17/', test17, name='test17'),
    
]
