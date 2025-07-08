from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
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
    """טופס ליצירת לקוח חדש ע"י מנהל/מכונאי - ללא חשבון משתמש"""
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        labels = {
            'name': 'שם',
            'phone': 'טלפון',
            'email': 'אימייל (לא חובה)',
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'לדוגמה: 050-1234567',
                'pattern': '[0-9\-\+]{9,15}'
            })
        }
    
    def save(self, commit=True):
        customer = super().save(commit=False)
        # לקוח זה נוצר ע"י מנהל/מכונאי - ללא קישור למשתמש
        customer.user = None  
        if commit:
            customer.save()
        return customer

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
    name = forms.CharField(label="שם מלא", max_length=100)
    phone = forms.CharField(
        label="טלפון",
        max_length=20,
        validators=[RegexValidator(r'^[0-9\-\+]{9,15}$', 'נא להזין מספר טלפון תקין')]
    )
    email = forms.EmailField(label="אימייל", required=False)
    
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'password1', 'password2')
        labels = {
            'username': 'שם משתמש',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "סיסמה"
        self.fields['password2'].label = "אימות סיסמה"

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'mechanic'})
        return user

class ManagerSignUpForm(UserCreationForm):
    """טופס הרשמת מנהל (role='manager')"""
    name = forms.CharField(label="שם מלא", max_length=100)
    phone = forms.CharField(
        label="טלפון",
        max_length=20,
        validators=[RegexValidator(r'^[0-9\-\+]{9,15}$', 'נא להזין מספר טלפון תקין')]
    )
    email = forms.EmailField(label="אימייל", required=False)
    
    class Meta:
        model = User
        fields = ('username', 'name', 'phone', 'email', 'password1', 'password2')
        labels = {
            'username': 'שם משתמש',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "סיסמה"
        self.fields['password2'].label = "אימות סיסמה"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True   # גישה ל־admin
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'manager'})
        return user

class CustomerRegisterForm(UserCreationForm):
    name = forms.CharField(label="שם מלא", max_length=100)
    phone = forms.CharField(
        label="טלפון",
        max_length=20,
        validators=[RegexValidator(r'^[0-9\-\+]{9,15}$', 'נא להזין מספר טלפון תקין')]
    )
    email = forms.EmailField(label="אימייל", required=False)
    
    # אפשרות לחבר לקוח קיים
    link_existing = forms.BooleanField(
        label="יש לי כבר פרטים במערכת",
        required=False,
        help_text="סמן אם אתה כבר רשום במערכת כלקוח (ע\"י המנהל) ורוצה לחבר את החשבון"
    )

    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2', 'link_existing']
        labels = {
            'username': 'שם משתמש',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "סיסמה"
        self.fields['password2'].label = "אימות סיסמה"

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        name = cleaned_data.get('name')
        link_existing = cleaned_data.get('link_existing')
        
        if link_existing and phone and name:
            # בדיקה אם יש לקוח קיים עם הפרטים האלה
            try:
                self.existing_customer = Customer.objects.get(
                    phone=phone,
                    user__isnull=True
                )
                # בדיקה שהשם דומה (לפחות השם הפרטי)
                if not any(part.lower() in self.existing_customer.name.lower() 
                          for part in name.split()):
                    raise forms.ValidationError(
                        f"נמצא לקוח עם הטלפון {phone} אבל השם לא תואם. "
                        f"השם במערכת: {self.existing_customer.name}"
                    )
            except Customer.DoesNotExist:
                raise forms.ValidationError(
                    f"לא נמצא לקוח במערכת עם הטלפון {phone}. "
                    "אם אתה בטוח שאתה רשום, פנה למנהל המוסך."
                )
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'customer'})
            
            # בדיקה אם צריך לחבר לקוח קיים
            if hasattr(self, 'existing_customer') and self.cleaned_data.get('link_existing'):
                # עדכון הלקוח הקיים עם המשתמש החדש
                self.existing_customer.user = user
                # עדכון פרטים אם שונים
                if self.existing_customer.email != self.cleaned_data['email']:
                    self.existing_customer.email = self.cleaned_data['email']
                self.existing_customer.save()
            else:
                # יצירת לקוח חדש
                Customer.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': self.cleaned_data['name'],
                        'phone': self.cleaned_data['phone'],
                        'email': self.cleaned_data['email'],
                    }
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

class CustomerLinkForm(forms.Form):
    """טופס לחיבור משתמש רשום ללקוח קיים"""
    phone = forms.CharField(
        label="טלפון (כפי שרשום במערכת)",
        max_length=20,
        help_text="הזן את מספר הטלפון שרשום במערכת"
    )
    name = forms.CharField(
        label="שם מלא (לאימות)",
        max_length=100,
        help_text="הזן את שמך המלא לאימות"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        name = cleaned_data.get('name')
        
        if phone and name:
            # חיפוש לקוח קיים ללא user
            try:
                self.existing_customer = Customer.objects.get(
                    phone=phone, 
                    name__icontains=name.split()[0],  # בדיקה לפי השם הפרטי
                    user__isnull=True
                )
            except Customer.DoesNotExist:
                raise forms.ValidationError(
                    "לא נמצא לקוח במערכת עם הפרטים האלה. "
                    "אולי הפרטים שונים או שכבר יש לך חשבון?"
                )
            except Customer.MultipleObjectsReturned:
                raise forms.ValidationError(
                    "נמצאו מספר לקוחות עם פרטים דומים. "
                    "אנא פנה למנהל המוסך לעזרה."
                )
        
        return cleaned_data
