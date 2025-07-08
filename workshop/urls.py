from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    
    # Home
    path("", views.home, name="home"),
    
    # Customer and Bikes
    path('customer/new/', views.customer_form, name='customer_form'),
    path('bike/new/', views.bike_form, name='bike_form'),
    
    # Repairs
    path('repair/new/', views.repair_form, name='repair_form'),
    path('customer/report/', views.customer_report, name='customer_report'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('subcategories/new/', views.subcategory_create, name='subcategory_create'),
]
