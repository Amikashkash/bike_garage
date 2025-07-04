from django.contrib import admin
from .models import (
    UserProfile,
    Customer,
    Bike,
    RepairCategory,
    RepairSubCategory,
    RepairJob,
)

# רישום מודלים לממשק הניהול
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Bike)
admin.site.register(RepairCategory)
admin.site.register(RepairSubCategory)
admin.site.register(RepairJob)
