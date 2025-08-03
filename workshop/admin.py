from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.admin import AdminSite
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

# Custom Admin Site for organized menu
class BikeGarageAdminSite(AdminSite):
    site_header = 'ניהול מוסך האופניים'
    site_title = 'מוסך האופניים'
    index_title = 'ברוכים הבאים למערכת ניהול המוסך'
    
    def index(self, request, extra_context=None):
        """Custom admin index with grouped content and counts"""
        extra_context = extra_context or {}
        
        # Get counts for display
        extra_context.update({
            'customer_count': Customer.objects.count(),
            'bike_count': Bike.objects.count(),
            'repair_count': RepairJob.objects.count(),
            'category_count': RepairCategory.objects.count(),
            'user_count': User.objects.count(),
        })
        
        # Get recent actions
        from django.contrib.admin.models import LogEntry
        extra_context['recent_actions'] = LogEntry.objects.select_related('user').order_by('-action_time')[:10]
        
        return super().index(request, extra_context)

# Create custom admin site instance
admin_site = BikeGarageAdminSite(name='bikegarage_admin')

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
    
    # תרגום כותרות עמודות לעברית
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

# Register models with custom admin site
from django.contrib.auth.models import Group
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

admin_site.register(User, UserAdmin)
admin_site.register(Group)
admin_site.register(Session)
admin_site.register(LogEntry)
admin_site.register(ContentType)

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
    list_display = ('name', 'phone', 'email', 'user', 'has_user_account')
    search_fields = ('name', 'phone', 'email')
    
    def has_user_account(self, obj):
        return obj.user is not None
    has_user_account.boolean = True
    has_user_account.short_description = 'יש חשבון משתמש'

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'color', 'customer', 'get_repairs_count')
    list_filter = ('brand', 'color')
    search_fields = ('brand', 'model', 'customer__name')
    
    def get_repairs_count(self, obj):
        return obj.repairjob_set.count()
    get_repairs_count.short_description = 'מספר תיקונים'

@admin.register(RepairCategory)
class RepairCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_subcategories_count')
    search_fields = ('name',)
    
    def get_subcategories_count(self, obj):
        return obj.subcategories.count()
    get_subcategories_count.short_description = 'מספר תת-קטגוריות'

@admin.register(RepairSubCategory)
class RepairSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_jobs_count')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    
    def get_jobs_count(self, obj):
        return obj.repair_jobs.count()
    get_jobs_count.short_description = 'מספר תיקונים'

@admin.register(RepairJob)
class RepairJobAdmin(admin.ModelAdmin):
    list_display = ('job_number', 'bike', 'customer_name', 'status', 'assigned_mechanic', 'is_stuck', 'created_at', 'get_total_price')
    list_filter = ('status', 'is_stuck', 'created_at', 'assigned_mechanic')
    search_fields = ('id', 'bike__brand', 'bike__customer__name', 'problem_description')
    readonly_fields = ('created_at', 'diagnosed_at', 'approved_at')
    ordering = ('-created_at',)
    filter_horizontal = ('subcategories',)
    
    fieldsets = (
        ('מידע בסיסי', {
            'fields': ('bike', 'subcategories', 'problem_description', 'diagnosis')
        }),
        ('סטטוס ומועדים', {
            'fields': ('status', 'assigned_mechanic', 'created_at', 'diagnosed_at', 'approved_at')
        }),
        ('תקיעות ובעיות', {
            'fields': ('is_stuck', 'stuck_reason', 'stuck_at', 'stuck_resolved', 'manager_response'),
            'classes': ('collapse',)
        }),
        ('בדיקת איכות', {
            'fields': ('quality_checked_by', 'quality_check_date', 'quality_notes', 'ready_for_pickup_date', 'customer_notified'),
            'classes': ('collapse',)
        }),
        ('תפיסה ראשונה', {
            'fields': ('available_for_pickup', 'pickup_priority'),
            'classes': ('collapse',)
        }),
    )
    
    def job_number(self, obj):
        """Display job number with # prefix"""
        return f"#{obj.id}"
    job_number.short_description = 'מספר תיקון'
    job_number.admin_order_field = 'id'
    
    def customer_name(self, obj):
        """Display customer name"""
        return obj.bike.customer.name
    customer_name.short_description = 'לקוח'
    customer_name.admin_order_field = 'bike__customer__name'
    
    def get_total_price(self, obj):
        """Display total price"""
    def get_total_price(self, obj):
        """Display total price"""
        return f"₪{obj.get_total_price()}"
    get_total_price.short_description = 'סה"כ מחיר'

@admin.register(RepairItem)
class RepairItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'job_number', 'price', 'is_approved_by_customer', 'status')
    list_filter = ('is_approved_by_customer', 'status', 'repair_job__status')
    search_fields = ('description', 'repair_job__id', 'repair_job__bike__customer__name')
    ordering = ('-repair_job__created_at',)
    
    def job_number(self, obj):
        """Display job number with # prefix"""
        return f"#{obj.repair_job.id}"
    job_number.short_description = 'מספר תיקון'
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
    job_number.short_description = 'מספר תיקון'
    job_number.admin_order_field = 'repair_job__id'
    
    def message_preview(self, obj):
        """Display first 50 characters of message"""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'תוכן ההודעה'

# הוספת כותרת מותאמת אישית לאדמין
admin.site.site_header = "🔧 מערכת ניהול מוסך אופניים"
admin.site.site_title = "מוסך אופניים - אדמין"
admin.site.index_title = "לוח בקרה ראשי"

# Add custom admin view
def get_admin_urls():
    from django.urls import path
    return [
        path('create-mechanic/', create_mechanic_view, name='create_mechanic'),
    ]

# Store the function for use in urls.py if needed
