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
    active_repairs_summary,
    subscribe_to_push_notifications,
    unsubscribe_from_push_notifications,
    push_subscription_status,
    vapid_public_key
)
from .api_management import (
    CategoryManagementListView,
    CategoryManagementDetailView,
    SubcategoryManagementListView,
    SubcategoryManagementDetailView,
    category_stats,
    batch_create_subcategories
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
    
    # Push notifications
    path('customer/push/subscribe/', subscribe_to_push_notifications, name='subscribe_push_notifications'),
    path('customer/push/unsubscribe/', unsubscribe_from_push_notifications, name='unsubscribe_push_notifications'),
    path('customer/push/status/', push_subscription_status, name='push_subscription_status'),
    path('vapid-public-key/', vapid_public_key, name='vapid_public_key'),
    
    # Repair categories (for creating new repairs)
    path('repair-categories/', RepairCategoryListView.as_view(), name='repair_categories'),
    path('repair-categories/<int:category_id>/subcategories/', RepairSubCategoryListView.as_view(), name='repair_subcategories'),
    
    # Management endpoints
    path('management/categories/', CategoryManagementListView.as_view(), name='management_categories'),
    path('management/categories/<int:pk>/', CategoryManagementDetailView.as_view(), name='management_category_detail'),
    path('management/categories/<int:category_id>/subcategories/', SubcategoryManagementListView.as_view(), name='management_subcategories'),
    path('management/subcategories/<int:pk>/', SubcategoryManagementDetailView.as_view(), name='management_subcategory_detail'),
    path('management/category-stats/', category_stats, name='category_stats'),
    path('management/subcategories/batch-create/', batch_create_subcategories, name='batch_create_subcategories'),
]