from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import RepairJob, RepairSubCategory, Bike
from django.contrib.auth.models import User
from .models import (
    Customer,
    Bike,
    RepairCategory,
    RepairSubCategory,
    RepairJob,
    UserProfile,
)

# -- טפסים למודלים עיקריים --

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
    subcategories = forms.ModelMultipleChoiceField(
        queryset=RepairSubCategory.objects.select_related('category'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="תקלות (בחירה מרשימת תתי־קטגוריות)"
    )

    class Meta:
        model = RepairJob
        fields = [
            'bike',                 # בוחר אופניים (עם שם הלקוח בצד ברשימה)
            'subcategories',        # רשימת תקלות
            'problem_description',  # תיאור
            'diagnosis',            # אבחון
            'quote_price',          # הצעת מחיר
            'is_approved',          # אישור
        ]
        labels = {
            'bike': 'אופניים',
            'problem_description': 'תיאור התקלה (חופשי)',
            'diagnosis': 'אבחון',
            'quote_price': 'הצעת מחיר',
            'is_approved': 'אושר על ידי הלקוח',
        }
        widgets = {
            'subcategories': forms.CheckboxSelectMultiple,
        }

# -- טפסי הרשמה והרשאות --

class MechanicSignUpForm(UserCreationForm):
    """טופס הרשמת מכונאי (role='mechanic')"""
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        Customer.objects.create(
            user=user,  # ← זהו הקישור החיוני!
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
        )
        return user

class ManagerSignUpForm(UserCreationForm):
    """טופס הרשמת מנהל (role='manager')"""
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True   # גישה ל־admin
        if commit:
            user.save()
            UserProfile.objects.create(user=user, role='manager')
        return user

class CustomerRegisterForm(UserCreationForm):
    name = forms.CharField(label="שם מלא", max_length=100)
    phone = forms.CharField(label="טלפון", max_length=20)
    email = forms.EmailField(label="אימייל", required=False)

    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2']
        labels = {
            'username': 'שם משתמש',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "סיסמה"
        self.fields['password2'].label = "אימות סיסמה"

    def save(self, commit=True):
        user = super().save(commit=commit)
        Customer.objects.create(
            user=user,  # ← קישור ה־User ל־Customer
            name=self.cleaned_data['name'],
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
        )
        return user
    
    
class CustomerRepairJobForm(forms.ModelForm):
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
        ]
        labels = {
            'bike': 'אופניים',
            'subcategories': 'תקלות',
            'problem_description': 'תיאור התקלה (חופשי)',
        }
    