from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    USER_ROLES = [
        ('customer', 'לקוח'),
        ('mechanic', 'מכונאי'),
        ('manager', 'מנהל'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Bike(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bikes')
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model or ''} ({self.customer.name})"


class RepairCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RepairSubCategory(models.Model):
    category = models.ForeignKey(
        RepairCategory,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return f"{self.category.name} > {self.name}"


class RepairJob(models.Model):
    STATUS_CHOICES = [
        ('reported', 'דווח על ידי לקוח'),
        ('diagnosed', 'מאובחן - ממתין לאישור לקוח'),
        ('partially_approved', 'אושר חלקית על ידי לקוח'),
        ('approved', 'אושר על ידי לקוח'),
        ('in_progress', 'בביצוע'),
        ('awaiting_quality_check', 'ממתין לבדיקת איכות'),
        ('quality_approved', 'עבר בדיקת איכות - מוכן לאיסוף'),
        ('completed', 'הושלם'),
        ('delivered', 'נמסר ללקוח'),
    ]
    
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    subcategories = models.ManyToManyField(
        RepairSubCategory,
        blank=True,
        related_name='repair_jobs'
    )
    problem_description = models.TextField(blank=True, verbose_name="תיאור התקלה")
    diagnosis = models.TextField(blank=True, verbose_name="אבחון")
    
    # פרטי סטטוס
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosed_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # משתמשים במעורבות
    assigned_mechanic = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_repairs'
    )
    
    # סטטוס "תקוע" למכונאי
    is_stuck = models.BooleanField(default=False, verbose_name="מכונאי תקוע")
    stuck_reason = models.TextField(blank=True, verbose_name="סיבת התקיעות")
    stuck_at = models.DateTimeField(null=True, blank=True, verbose_name="תאריך סימון כתקוע")
    stuck_resolved = models.BooleanField(default=False, verbose_name="התקיעות נפתרה")
    manager_response = models.TextField(blank=True, verbose_name="תגובת מנהל")
    
    # בדיקת איכות על ידי מנהל
    quality_checked_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quality_checked_repairs',
        verbose_name="נבדק על ידי מנהל"
    )
    quality_check_date = models.DateTimeField(null=True, blank=True, verbose_name="תאריך בדיקת איכות")
    quality_notes = models.TextField(blank=True, verbose_name="הערות בדיקת איכות")
    ready_for_pickup_date = models.DateTimeField(null=True, blank=True, verbose_name="תאריך מוכנות לאיסוף")
    customer_notified = models.BooleanField(default=False, verbose_name="לקוח עודכן על מוכנות לאיסוף")
    
    # שדות לתפיסה ראשונה
    available_for_pickup = models.BooleanField(default=False, verbose_name="זמין לתפיסה ראשונה")
    pickup_priority = models.CharField(
        max_length=20,
        choices=[
            ('normal', 'רגיל'),
            ('urgent', 'דחוף'),
            ('critical', 'קריטי')
        ],
        default='normal',
        verbose_name="עדיפות"
    )

    def __str__(self):
        return f"תיקון {self.bike} - {self.get_status_display()}"
    
    def get_total_price(self):
        """סה"כ מחיר כל הפעולות"""
        return sum(item.price for item in self.repair_items.all())
    
    def get_total_approved_price(self):
        """מחיר כל הפעולות שאושרו"""
        return sum(item.price for item in self.repair_items.filter(is_approved_by_customer=True))
    
    def get_pending_approval_price(self):
        """מחיר פעולות שממתינות לאישור"""
        return sum(item.price for item in self.repair_items.filter(is_approved_by_customer=False))
    
    def get_completed_count(self):
        """מספר פעולות שהושלמו"""
        return self.repair_items.filter(is_completed=True).count()
    
    def get_approved_count(self):
        """מספר פעולות מאושרות"""
        return self.repair_items.filter(is_approved_by_customer=True).count()
    
    def get_progress_percentage(self):
        """אחוז ההתקדמות"""
        approved = self.get_approved_count()
        if approved == 0:
            return 0
        completed = self.get_completed_count()
        return (completed / approved) * 100
    
    @property
    def progress_percentage(self):
        """property לגישה קלה מהתבניות"""
        return self.get_progress_percentage()
    
    @property  
    def is_effectively_stuck(self):
        """האם התיקון תקוע למעשה (תקוע או יש פעולות חסומות)"""
        if self.is_stuck:
            return True
        # בדיקה אם יש פעולות חסומות
        return self.repair_items.filter(status='blocked').exists()
    
    @property
    def completed_items(self):
        """פעולות שהושלמו"""
        return self.repair_items.filter(status='completed')
        
    @property
    def approved_items(self):
        """פעולות מאושרות"""
        return self.repair_items.filter(is_approved_by_customer=True)
        
    @property
    def blocked_items(self):
        """פעולות חסומות"""
        return self.repair_items.filter(status='blocked')
    
    @property
    def has_blocked_items(self):
        """האם יש פעולות חסומות"""
        return self.blocked_items.exists()

    # ...existing code...


class RepairItem(models.Model):
    """פעולה/חלק בתיקון"""
    STATUS_CHOICES = [
        ('pending', 'ממתין'),
        ('completed', 'בוצע'),
        ('blocked', 'תקוע'),
    ]
    
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name='repair_items')
    description = models.CharField(max_length=200, verbose_name="תיאור הפעולה")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="מחיר")
    is_approved_by_customer = models.BooleanField(default=False, verbose_name="אושר על ידי לקוח")
    
    # סטטוס הפעולה
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="סטטוס")
    
    # שדות ישנים לתאימות לאחור
    is_completed = models.BooleanField(default=False, verbose_name="בוצע")
    completed_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="בוצע על ידי"
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, verbose_name="הערות")

    def save(self, *args, **kwargs):
        """שמירה עם עדכון שדות ישנים לתאימות לאחור"""
        # עדכון is_completed בהתאם לסטטוס
        self.is_completed = (self.status == 'completed')
        super().save(*args, **kwargs)
        
        # עדכון סטטוס "תקוע" של התיקון כולו
        self._update_repair_job_stuck_status()
    
    def _update_repair_job_stuck_status(self):
        """עדכון סטטוס התקיעות של התיקון כולו בהתאם לפעולות חסומות"""
        from django.utils import timezone
        
        # בדיקה אם יש פעולות חסומות
        has_blocked_items = self.repair_job.repair_items.filter(status='blocked').exists()
        
        if has_blocked_items and not self.repair_job.is_stuck:
            # יש פעולות חסומות והתיקון עדיין לא מסומן כתקוע
            self.repair_job.is_stuck = True
            self.repair_job.stuck_reason = 'התיקון מכיל פעולות חסומות הדורשות התייחסות מנהל'
            self.repair_job.stuck_at = timezone.now()
            self.repair_job.stuck_resolved = False
            self.repair_job.save()
        elif not has_blocked_items and self.repair_job.is_stuck and not self.repair_job.stuck_resolved:
            # אין פעולות חסומות והתיקון עדיין מסומן כתקוע (אבל לא נפתר על ידי מנהל)
            self.repair_job.is_stuck = False
            self.repair_job.stuck_reason = ''
            self.repair_job.stuck_at = None
            self.repair_job.save()
    
    def mark_as_completed(self, user=None):
        """סימון כבוצע"""
        self.status = 'completed'
        self.is_completed = True
        if user:
            self.completed_by = user
        from django.utils import timezone
        self.completed_at = timezone.now()
        self.save()
    
    def mark_as_blocked(self, reason=""):
        """סימון כתקוע"""
        self.status = 'blocked'
        self.is_completed = False
        if reason:
            self.notes = reason
        self.save()
    
    def mark_as_pending(self):
        """סימון כממתין"""
        self.status = 'pending'
        self.is_completed = False
        self.save()

    def __str__(self):
        return f"{self.description} - ₪{self.price}"


class RepairUpdate(models.Model):
    """עדכונים על התיקון"""
    repair_job = models.ForeignKey(RepairJob, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField(verbose_name="הודעה")
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible_to_customer = models.BooleanField(default=True, verbose_name="גלוי ללקוח")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"עדכון על {self.repair_job} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
