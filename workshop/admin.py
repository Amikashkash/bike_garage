from django.contrib import admin
from .models import (
    UserProfile,
    Customer,
    Bike,
    RepairCategory,
    RepairSubCategory,
    RepairJob,
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'user')
    search_fields = ('name', 'phone', 'email')

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'color', 'customer')
    list_filter = ('brand',)
    search_fields = ('brand', 'model', 'customer__name')

@admin.register(RepairCategory)
class RepairCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(RepairSubCategory)
class RepairSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(RepairJob)
class RepairJobAdmin(admin.ModelAdmin):
    list_display = ('bike', 'is_approved', 'quote_price', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('bike__brand', 'bike__customer__name')
    readonly_fields = ('created_at',)
