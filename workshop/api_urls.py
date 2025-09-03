from django.urls import path
from .api_customer import (
    customer_stats,
    CustomerRepairListView,
    CustomerRepairDetailView,
    approve_repair_items,
    CustomerNotificationListView,
    mark_notification_read,
    mark_all_notifications_read,
    RepairCategoryListView,
    RepairSubCategoryListView,
    active_repairs_summary
)

app_name = 'api'

urlpatterns = [
    # Customer stats for home page
    path('customer/stats/', customer_stats, name='customer_stats'),
    
    # Repair management
    path('customer/repairs/', CustomerRepairListView.as_view(), name='customer_repairs'),
    path('customer/repairs/<int:pk>/', CustomerRepairDetailView.as_view(), name='customer_repair_detail'),
    path('customer/repairs/<int:repair_id>/approve/', approve_repair_items, name='approve_repair_items'),
    path('customer/repairs/active/summary/', active_repairs_summary, name='active_repairs_summary'),
    
    # Notifications
    path('customer/notifications/', CustomerNotificationListView.as_view(), name='customer_notifications'),
    path('customer/notifications/<int:notification_id>/read/', mark_notification_read, name='mark_notification_read'),
    path('customer/notifications/read-all/', mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Repair categories (for creating new repairs)
    path('repair-categories/', RepairCategoryListView.as_view(), name='repair_categories'),
    path('repair-categories/<int:category_id>/subcategories/', RepairSubCategoryListView.as_view(), name='repair_subcategories'),
]