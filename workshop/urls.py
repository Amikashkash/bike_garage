from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("", views.home, name="home"),
    path('customer/new/', views.customer_form, name='customer_form'),
    path('bike/new/', views.bike_form, name='bike_form'),
    path('repair/new/', views.repair_form, name='repair_form'),

    
    # נחזיר את הטפסים בהמשך ונוסיף כאן לינקים אליהם
]
