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
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/link/', views.link_customer_to_user, name='link_customer_user'),
    path('bike/new/', views.bike_form, name='bike_form'),
    
    # Customer and Bike management (for managers)
    path('manager/customer-bike/new/', views.customer_with_bike_form, name='customer_with_bike_new'),
    path('manager/customer/<int:customer_id>/bike/<int:bike_id>/edit/', views.customer_with_bike_form, name='customer_with_bike_edit'),
    path('manager/customer/<int:customer_id>/bike/new/', views.customer_with_bike_form, name='customer_bike_add'),
    
    # Customer bike management (for customers)
    path('my-bikes/', views.customer_bikes_list, name='customer_bikes_list'),
    path('my-bikes/add/', views.customer_add_bike, name='customer_add_bike'),
    
    # Repairs
    path('repair/new/', views.repair_form, name='repair_form'),
    path('customer/report/', views.customer_report, name='customer_report'),
    path('repair/<int:repair_id>/status/', views.repair_status, name='repair_status'),
    
    # Manager workflow
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/repair/<int:repair_id>/diagnosis/', views.repair_diagnosis, name='repair_diagnosis'),
    path('manager/repair/<int:repair_id>/assign/', views.assign_mechanic, name='assign_mechanic'),
    path('manager/response-stuck/', views.manager_response_stuck, name='manager_response_stuck'),
    
    # Customer approval
    path('repair/<int:repair_id>/approve/', views.customer_approval, name='customer_approval'),
    
    # Mechanic workflow
    path('mechanic/dashboard/', views.mechanic_dashboard, name='mechanic_dashboard'),
    path('mechanic/repair/<int:repair_id>/complete/', views.mechanic_task_completion, name='mechanic_task_completion'),
    path('mechanic/update-status/', views.update_repair_status, name='update_repair_status'),
    
    # Manager quality check
    path('manager/quality-check/<int:repair_id>/', views.manager_quality_check, name='manager_quality_check'),
    path('manager/quality-approve/<int:repair_id>/', views.manager_quality_approve, name='manager_quality_approve'),
    path('manager/notify-customer/<int:repair_id>/', views.manager_notify_customer, name='manager_notify_customer'),
    path('manager/mark-delivered/<int:repair_id>/', views.manager_mark_delivered, name='manager_mark_delivered'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('subcategories/new/', views.subcategory_create, name='subcategory_create'),
]
