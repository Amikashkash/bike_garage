from rest_framework import serializers
from .models import (
    Customer, Bike, RepairJob, RepairItem, RepairCategory, 
    RepairSubCategory, CustomerNotification, RepairUpdate
)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email']


class BikeSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = Bike
        fields = ['id', 'brand', 'model', 'color', 'customer_name']


class RepairCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairCategory
        fields = ['id', 'name']


class RepairSubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = RepairSubCategory
        fields = ['id', 'name', 'category_name', 'category']


class RepairItemSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    completed_by_name = serializers.CharField(source='completed_by.username', read_only=True)
    
    class Meta:
        model = RepairItem
        fields = [
            'id', 'description', 'price', 'is_approved_by_customer',
            'status', 'status_display', 'is_completed', 'completed_by_name',
            'completed_at', 'notes'
        ]


class RepairUpdateSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_role = serializers.SerializerMethodField()
    
    class Meta:
        model = RepairUpdate
        fields = [
            'id', 'message', 'created_at', 'is_visible_to_customer',
            'user_name', 'user_role'
        ]
    
    def get_user_role(self, obj):
        if hasattr(obj.user, 'userprofile'):
            return obj.user.userprofile.get_role_display()
        return 'משתמש'


class RepairJobSerializer(serializers.ModelSerializer):
    bike_info = BikeSerializer(source='bike', read_only=True)
    subcategories_list = RepairSubCategorySerializer(source='subcategories', many=True, read_only=True)
    repair_items = RepairItemSerializer(many=True, read_only=True)
    updates = RepairUpdateSerializer(many=True, read_only=True)
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_mechanic_name = serializers.CharField(source='assigned_mechanic.username', read_only=True)
    quality_checked_by_name = serializers.CharField(source='quality_checked_by.username', read_only=True)
    
    # Computed fields
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    total_approved_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    pending_approval_price = serializers.DecimalField(max_digits=8, decimal_places=2, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    completed_items_count = serializers.IntegerField(read_only=True)
    approved_items_count = serializers.IntegerField(read_only=True)
    is_effectively_stuck = serializers.BooleanField(read_only=True)
    has_blocked_items = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = RepairJob
        fields = [
            'id', 'problem_description', 'diagnosis', 'status', 'status_display',
            'created_at', 'diagnosed_at', 'approved_at', 'ready_for_pickup_date',
            'customer_notified', 'available_for_pickup', 'pickup_priority',
            'is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response',
            'quality_check_date', 'quality_notes',
            'bike_info', 'subcategories_list', 'repair_items', 'updates',
            'assigned_mechanic_name', 'quality_checked_by_name',
            'total_price', 'total_approved_price', 'pending_approval_price',
            'progress_percentage', 'completed_items_count', 'approved_items_count',
            'is_effectively_stuck', 'has_blocked_items'
        ]


class CustomerNotificationSerializer(serializers.ModelSerializer):
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    repair_info = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomerNotification
        fields = [
            'id', 'notification_type', 'notification_type_display', 'title', 'message',
            'is_read', 'read_at', 'is_clicked', 'clicked_at', 'created_at',
            'action_url', 'repair_info'
        ]
    
    def get_repair_info(self, obj):
        if obj.repair_job:
            return {
                'id': obj.repair_job.id,
                'bike_brand': obj.repair_job.bike.brand,
                'bike_model': obj.repair_job.bike.model,
                'status': obj.repair_job.get_status_display()
            }
        return None


class CustomerStatsSerializer(serializers.Serializer):
    active_repairs = serializers.IntegerField()
    total_repairs = serializers.IntegerField()
    notifications = serializers.IntegerField()
    ready_for_pickup = serializers.IntegerField()