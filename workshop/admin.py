from django.contrib import admin
from .models import Customer, Bike, ProblemType, RepairJob
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


admin.site.register(Customer)
admin.site.register(Bike)
admin.site.register(ProblemType)
admin.site.register(RepairJob)
