from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import (
    UserProfile,
    Customer,
    Bike,
    RepairCategory,
    RepairSubCategory,
    RepairJob,
    RepairItem,
    RepairUpdate,
)

# פונקציית עזר ליצירת טכנאי מהירה
def create_mechanic_view(request):
    """ממשק ליצירת טכנאי מהירה"""
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', 'טכנאי')
        last_name = request.POST.get('last_name', 'חדש')
        email = request.POST.get('email', f'{username}@bikegarage.test')
        password = request.POST.get('password', 'test123')
        
        if username:
            try:
                # בדיקה אם קיים
                if User.objects.filter(username=username).exists():
                    return HttpResponse(f"❌ שם המשתמש {username} כבר קיים!")
                
                # יצירת משתמש
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # יצירת פרופיל טכנאי
                UserProfile.objects.create(user=user, role='mechanic')
                
                return HttpResponse(f"✅ נוצר טכנאי חדש: {username} (סיסמה: {password})")
                
            except Exception as e:
                return HttpResponse(f"❌ שגיאה: {e}")
    
    # טופס HTML פשוט
    html = """
    <html>
    <head>
        <title>יצירת טכנאי חדש</title>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial; padding: 20px; direction: rtl;">
        <h2>🔧 יצירת טכנאי חדש</h2>
        <form method="post">
            <table style="border-spacing: 10px;">
                <tr><td>שם משתמש:</td><td><input type="text" name="username" required style="width: 200px;"></td></tr>
                <tr><td>שם פרטי:</td><td><input type="text" name="first_name" value="טכנאי" style="width: 200px;"></td></tr>
                <tr><td>שם משפחה:</td><td><input type="text" name="last_name" value="חדש" style="width: 200px;"></td></tr>
                <tr><td>אימייל:</td><td><input type="email" name="email" placeholder="username@bikegarage.test" style="width: 200px;"></td></tr>
                <tr><td>סיסמה:</td><td><input type="text" name="password" value="test123" style="width: 200px;"></td></tr>
                <tr><td colspan="2"><button type="submit" style="padding: 10px 20px; background: #007cba; color: white; border: none; border-radius: 5px;">יצירת טכנאי</button></td></tr>
            </table>
        </form>
        <p><a href="/admin/" style="color: #007cba;">← חזרה לאדמין</a></p>
    </body>
    </html>
    """
    return HttpResponse(html)

# Inline עבור UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'פרופיל משתמש'
    fields = ('role',)

# פעולות אדמין מותאמות אישית
def make_mechanic(modeladmin, request, queryset):
    """הפיכת משתמשים נבחרים לטכנאים"""
    count = 0
    for user in queryset:
        try:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if profile.role != 'mechanic' or created:
                profile.role = 'mechanic'
                profile.save()
                count += 1
        except:
            pass
    
    modeladmin.message_user(request, f'הופכו {count} משתמשים לטכנאים')

make_mechanic.short_description = "🔧 הפוך לטכנאי"

def make_manager(modeladmin, request, queryset):
    """הפיכת משתמשים נבחרים למנהלים"""
    count = 0
    for user in queryset:
        try:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if profile.role != 'manager' or created:
                profile.role = 'manager'
                profile.save()
                count += 1
        except:
            pass
    
    modeladmin.message_user(request, f'הופכו {count} משתמשים למנהלים')

make_manager.short_description = "👨‍💼 הפוך למנהל"

def make_customer(modeladmin, request, queryset):
    """הפיכת משתמשים נבחרים ללקוחות"""
    count = 0
    for user in queryset:
        try:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if profile.role != 'customer' or created:
                profile.role = 'customer'
                profile.save()
                count += 1
        except:
            pass
    
    modeladmin.message_user(request, f'הופכו {count} משתמשים ללקוחות')

make_customer.short_description = "🚴‍♂️ הפוך ללקוח"

# הרחבת UserAdmin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'userprofile__role')
    actions = [make_mechanic, make_manager, make_customer]
    
    def get_role(self, obj):
        try:
            return obj.userprofile.get_role_display()
        except UserProfile.DoesNotExist:
            return 'ללא תפקיד'
    get_role.short_description = 'תפקיד'
    get_role.admin_order_field = 'userprofile__role'

# ביטול רישום של User הקיים ורישום מחדש עם הרחבה
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_role_display', 'user_email', 'user_full_name')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'אימייל'
    
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip()
    user_full_name.short_description = 'שם מלא'

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
    list_display = ('job_number', 'bike', 'customer_name', 'status', 'assigned_mechanic', 'is_stuck', 'created_at')
    list_filter = ('status', 'is_stuck', 'created_at', 'assigned_mechanic')
    search_fields = ('id', 'bike__brand', 'bike__customer__name')
    readonly_fields = ('created_at', 'diagnosed_at', 'approved_at')
    ordering = ('-created_at',)
    
    def job_number(self, obj):
        """Display job number with # prefix"""
        return f"#{obj.id}"
    job_number.short_description = 'Job #'
    job_number.admin_order_field = 'id'
    
    def customer_name(self, obj):
        """Display customer name"""
        return obj.bike.customer.name
    customer_name.short_description = 'Customer'
    customer_name.admin_order_field = 'bike__customer__name'

@admin.register(RepairItem)
class RepairItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'job_number', 'price', 'is_approved_by_customer', 'status')
    list_filter = ('is_approved_by_customer', 'status', 'repair_job__status')
    search_fields = ('description', 'repair_job__id', 'repair_job__bike__customer__name')
    ordering = ('-repair_job__created_at',)
    
    def job_number(self, obj):
        """Display job number with # prefix"""
        return f"#{obj.repair_job.id}"
    job_number.short_description = 'Job #'
    job_number.admin_order_field = 'repair_job__id'

@admin.register(RepairUpdate)
class RepairUpdateAdmin(admin.ModelAdmin):
    list_display = ('job_number', 'user', 'message_preview', 'created_at', 'is_visible_to_customer')
    list_filter = ('is_visible_to_customer', 'created_at')
    search_fields = ('repair_job__id', 'repair_job__bike__customer__name', 'message')
    ordering = ('-created_at',)
    
    def job_number(self, obj):
        """Display job number with # prefix"""
        return f"#{obj.repair_job.id}"
    job_number.short_description = 'Job #'
    job_number.admin_order_field = 'repair_job__id'
    
    def message_preview(self, obj):
        """Display first 50 characters of message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

# הוספת כותרת מותאמת אישית לאדמין
admin.site.site_header = "🔧 מערכת ניהול מוסך אופניים"
admin.site.site_title = "מוסך אופניים"
admin.site.index_title = "לוח ניהול מוסך"
