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
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    subcategories = models.ManyToManyField(
        RepairSubCategory,
        blank=True,
        related_name='repair_jobs'
    )
    problem_description = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    quote_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repair for {self.bike}"
