from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
import os
from . import views
from .icon_views import app_icon_view
from . import notification_views
from . import demo_views
from . import api_views
# from . import system_views  # Temporarily disabled to fix deployment

def serve_sw_js(request):
    """Serve service worker with proper encoding"""
    try:
        sw_path = os.path.join(settings.BASE_DIR, 'workshop/static/sw.js')
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='application/javascript; charset=utf-8')
    except Exception as e:
        return HttpResponse(f'// Service worker error: {str(e)}', content_type='application/javascript')

def health_check(request):
    """Simple health check endpoint for Fly.io"""
    return HttpResponse("OK", content_type="text/plain")

urlpatterns = [
    # Health check for Fly.io (both with and without trailing slash)
    path('health/', health_check, name='health_check'),
    path('health', health_check, name='health_check_no_slash'),
    
    # PWA Service Worker - Fixed encoding
    path('sw.js', serve_sw_js, name='service_worker'),
    
    # PWA App Icon
    path('app-icon.svg', app_icon_view, name='app_icon'),
    
    # Authentication
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    
    # Home
    path("", views.home, name="home"),
    
    # System Status and Testing - Disabled until deployment issue is resolved
    # path('system/status/', system_views.system_status, name='system_status'),
    # path('system/test-notification/', system_views.test_notification_api, name='test_notification_api'),
    
    # Demo and Testing
    path('demo/notifications/', demo_views.notification_demo, name='notification_demo'),
    path('demo/send-notification/', demo_views.send_demo_notification, name='send_demo_notification'),
    
    # Customer and Bikes
    path('customer/new/', views.customer_form, name='customer_form'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/link/', views.link_customer_to_user, name='link_customer_user'),
    path('bike/new/', views.bike_form, name='bike_form'),
     path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    
    # Customer and Bike management (for managers)
    path('manager/customer-bike/new/', views.customer_with_bike_form, name='customer_with_bike_new'),
    path('manager/customer/<int:customer_id>/bike/<int:bike_id>/edit/', views.customer_with_bike_form, name='customer_with_bike_edit'),
    path('manager/customer/<int:customer_id>/bike/new/', views.customer_with_bike_form, name='customer_bike_add'),
    
    # Customer bike management (for customers)
    path('my-bikes/', views.customer_bikes_list, name='customer_bikes_list'),
    path('my-bikes/add/', views.customer_add_bike, name='customer_add_bike'),
    
    # Repairs
    path('repair/new/', views.repair_form, name='repair_form'),
    path('repair/new/<int:customer_id>/', views.repair_form, name='repair_form_with_customer'),
    path('customer/report/', views.customer_report, name='customer_report'),
    path('customer/report/done/', views.customer_report_done, name='customer_report_done'),
    path('repair/<int:repair_id>/status/', views.repair_status, name='repair_status'),
    
    # Manager workflow
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/dashboard/react/', views.manager_dashboard_react, name='manager_dashboard_react'),
    path('manager/repair/<int:repair_id>/', views.manager_repair_detail, name='manager_repair_detail'),
    path('manager/repair/<int:repair_id>/diagnosis/', views.repair_diagnosis, name='repair_diagnosis'),
    path('manager/repair/<int:repair_id>/assign/', views.assign_mechanic, name='assign_mechanic'),
    path('manager/response-stuck/', views.manager_response_stuck, name='manager_response_stuck'),
    
    # Print labels
    path('repair/<int:repair_id>/print-label/', views.print_bike_label, name='print_bike_label'),
    path('print-labels/', views.print_labels_menu, name='print_labels_menu'),
    
    # Backup system
    path('backup/', views.backup_menu, name='backup_menu'),
    path('backup/customers/', views.backup_customer_data, name='backup_customer_data'),
    path('backup/customers-csv/', views.backup_customers_csv, name='backup_customers_csv'),
    
    # Customer approval
    path('repair/<int:repair_id>/approve/', views.customer_approval, name='customer_approval'),
    
    # Mechanic workflow
    path('mechanic/dashboard/legacy/', views.mechanic_dashboard, name='mechanic_dashboard_legacy'),
    path('mechanic/dashboard/', views.mechanic_dashboard_react, name='mechanic_dashboard'),
    path('mechanic/dashboard/react/', views.mechanic_dashboard_react, name='mechanic_dashboard_react'),
    path('mechanic/repair/<int:repair_id>/complete/', views.mechanic_task_completion, name='mechanic_task_completion'),
    path('mechanic/update-status/', views.update_repair_status, name='update_repair_status'),
    
    # Manager quality check
    path('manager/quality-check/<int:repair_id>/', views.manager_quality_check, name='manager_quality_check'),
    path('manager/quality-approve/<int:repair_id>/', views.manager_quality_approve, name='manager_quality_approve'),
    path('manager/notify-customer/<int:repair_id>/', views.manager_notify_customer, name='manager_notify_customer'),
    path('manager/mark-delivered/<int:repair_id>/', views.manager_mark_delivered, name='manager_mark_delivered'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/react/', views.category_list_react, name='category_list_react'),
    path('categories/legacy/', views.category_list, name='category_list_legacy'),
    path('categories/new/', views.category_create, name='category_create'),
    path('subcategories/new/', views.subcategory_create, name='subcategory_create'),
    path('subcategories/react/', views.subcategory_create_react, name='subcategory_create_react'),
    path('subcategories/legacy/', views.subcategory_create, name='subcategory_create_legacy'),
    
    # API endpoints
    path('api/search-customers/', views.search_customers_api, name='search_customers_api'),
    path('api/customer-bikes/<int:customer_id>/', views.customer_bikes_api, name='customer_bikes_api'),
    
    # Notification API endpoints
    path('api/notifications/vapid-key/', notification_views.get_vapid_public_key, name='get_vapid_public_key'),
    path('api/notifications/subscribe/', notification_views.register_push_subscription, name='register_push_subscription'),
    path('api/notifications/unsubscribe/', notification_views.unregister_push_subscription, name='unregister_push_subscription'),
    path('api/notifications/', notification_views.get_notifications, name='get_notifications'),
    path('api/notifications/mark-read/', notification_views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/mark-all-read/', notification_views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('api/notifications/test/', notification_views.test_notification, name='test_notification'),
    
    # Real-time API endpoints
    path('api/manager/stats/', api_views.manager_stats, name='api_manager_stats'),
    path('api/manager/dashboard/', api_views.manager_dashboard_data, name='api_manager_dashboard'),
    path('api/customer/active-repairs/', api_views.customer_active_repairs, name='api_customer_active_repairs'),
    path('api/customer/bikes/', api_views.customer_bikes, name='api_customer_bikes'),
    path('api/customer/report/', api_views.customer_report_submit, name='api_customer_report_submit'),
    path('api/customer/notifications/', api_views.customer_notifications, name='api_customer_notifications'),
    path('api/customer/notifications/list/', api_views.customer_notifications_list, name='api_customer_notifications_list'),
    path('api/customer/notifications/mark-read/', api_views.mark_notification_read, name='api_mark_notification_read'),
    path('api/categories/', api_views.categories_list, name='api_categories_list'),
    path('api/repair/submit/', api_views.repair_form_submit, name='api_repair_form_submit'),
    path('api/mechanic/stats/', api_views.mechanic_stats, name='api_mechanic_stats'),
    path('api/mechanic/dashboard/', api_views.mechanic_dashboard_data, name='api_mechanic_dashboard'),
    path('api/mechanic/repair/<int:repair_id>/stuck/', api_views.report_stuck_repair, name='api_report_stuck_repair'),
    path('api/manager/resolve-stuck/<int:repair_id>/', api_views.resolve_stuck_repair, name='api_resolve_stuck_repair'),
    
    # Django REST Framework API endpoints
    path('api/', include('workshop.api_urls')),
]
