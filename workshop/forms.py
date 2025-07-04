from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    Customer,
    Bike,
    RepairCategory,
    RepairSubCategory,
    RepairJob,
    UserProfile,
)

# ——— Forms for domain models ———

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        labels = {
            'name' : 'שם',
            'phone': 'טלפון',
            'email': 'אימייל (לא חובה)',
        }

class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['customer', 'brand', 'model', 'color']
        labels = {
            'customer': 'לקוח',
            'brand'   : 'יצרן',
            'model'   : 'מודל (לא חובה)',
            'color'   : 'צבע (לא חובה)',
        }

class RepairCategoryForm(forms.ModelForm):
    class Meta:
        model = RepairCategory
        fields = ['name']
        labels = {
            'name': 'קטגוריה',
        }

class RepairSubCategoryForm(forms.ModelForm):
    class Meta:
        model = RepairSubCategory
        fields = ['category', 'name']
        labels = {
            'category': 'קטגוריה עליונה',
            'name'    : 'תת־קטגוריה',
        }


class RepairJobForm(forms.ModelForm):
    # שדה מותאם ל-ManyToMany לתתי־קטגוריות
    subcategories = forms.ModelMultipleChoiceField(
        queryset=RepairSubCategory.objects.select_related('category'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="תקלות (בחירה מרשימת תתי־קטגוריות)"
    )

    class Meta:
        model = RepairJob
        fields = [
            'bike',
            'subcategories',
            'problem_description',
            'diagnosis',
            'quote_price',
            'is_approved',
        ]
        labels = {
            'bike'               : 'אופניים',
            'problem_description': 'תיאור התקלה (חופשי)',
            'diagnosis'          : 'אבחון',
            'quote_price'        : 'הצעת מחיר',
            'is_approved'        : 'אושר על ידי הלקוח',
        }
        widgets = {
            # ניתן להגדיר כאן אם תרצה סידור שונה
            'subcategories': forms.CheckboxSelectMultiple,
        }

# ——— (אופציונלי) Forms ל-User/UserProfile ———

class MechanicSignUpForm(UserCreationForm):
    """טופס הרשמת מכונאי (role='mechanic')"""
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        # אם תרצה לאפשר כניסה ל-admin, השתמש user.is_staff = True
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role='mechanic')
        return user

class ManagerSignUpForm(UserCreationForm):
    """טופס הרשמת מנהל (role='manager')"""
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True   # גישה ל־admin
        # user.is_superuser = True  # אם תרצה מנהל־על
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role='manager')
        return user
