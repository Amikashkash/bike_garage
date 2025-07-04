from django.db import models
from django.contrib.auth.models import User
from django.db import models

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
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name
    

class Bike(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.customer.name})"

class ProblemType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class RepairJob(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    problem_types = models.ManyToManyField(ProblemType, blank=True)
    problem_description = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    quote_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repair for {self.bike}"
