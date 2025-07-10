from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Customer,
    Bike,
    RepairCategory,
    RepairSubCategory,
    RepairJob,
    UserProfile,
    RepairItem,
)

class AccordionCheckboxSelectMultiple(CheckboxSelectMultiple):
    """Widget שמציג תתי קטגוריות באקורדיון מאורגן לפי קטגוריות"""
    
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        
        # קבלת כל התתי קטגוריות מאורגנות לפי קטגוריה
        categories = {}
        for choice in self.choices:
            choice_value, choice_label = choice
            # פירוק התווית לקטגוריה ותת קטגוריה
            if ' > ' in choice_label:
                category_name, subcategory_name = choice_label.split(' > ', 1)
            else:
                category_name, subcategory_name = 'כללי', choice_label
            
            if category_name not in categories:
                categories[category_name] = []
            
            categories[category_name].append({
                'value': choice_value,
                'label': subcategory_name,
                'checked': choice_value in value
            })
        
        # בניית HTML לאקורדיון
        html_parts = []
        
        for category_name, subcategories in categories.items():
            category_id = f"category_{category_name.replace(' ', '_')}"
            
            # כותרת קטגוריה
            html_parts.append(f'''
                <div class="accordion-category">
                    <div class="accordion-header" onclick="toggleCategory('{category_id}')">
                        <span class="category-name">{category_name}</span>
                        <span class="accordion-arrow" id="arrow_{category_id}">▼</span>
                    </div>
                    <div class="accordion-content" id="{category_id}" style="display: none;">
            ''')
            
            # תתי קטגוריות
            for subcategory in subcategories:
                checked = 'checked' if subcategory['checked'] else ''
                html_parts.append(f'''
                    <div class="subcategory-item">
                        <label>
                            <input type="checkbox" name="{name}" value="{subcategory['value']}" {checked}>
                            <span class="subcategory-label">{subcategory['label']}</span>
                        </label>
                    </div>
                ''')
            
            html_parts.append('</div></div>')
        
        # הוספת CSS ו-JavaScript לאקורדיון
        html_parts.insert(0, '''
            <style>
                .accordion-category {
                    margin-bottom: 10px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    overflow: hidden;
                }
                
                .accordion-header {
                    background-color: #007bff;
                    color: white;
                    padding: 12px 15px;
                    cursor: pointer;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-weight: bold;
                }
                
                .accordion-header:hover {
                    background-color: #0056b3;
                }
                
                .accordion-content {
                    background-color: #f8f9fa;
                    padding: 10px;
                }
                
                .subcategory-item {
                    padding: 8px 0;
                    border-bottom: 1px solid #e9ecef;
                }
                
                .subcategory-item:last-child {
                    border-bottom: none;
                }
                
                .subcategory-item label {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                    margin: 0;
                }
                
                .subcategory-item input[type="checkbox"] {
                    margin-left: 10px;
                    margin-right: 0;
                    transform: scale(1.2);
                }
                
                .subcategory-label {
                    flex-grow: 1;
                    padding-right: 10px;
                }
                
                @media (max-width: 768px) {
                    .accordion-header {
                        font-size: 14px;
                        padding: 10px 12px;
                    }
                    
                    .subcategory-item input[type="checkbox"] {
                        transform: scale(1.3);
                        margin-left: 12px;
                    }
                }
            </style>
            
            <script>
                function toggleCategory(categoryId) {
                    const content = document.getElementById(categoryId);
                    const arrow = document.getElementById('arrow_' + categoryId);
                    
                    if (content.style.display === 'none') {
                        content.style.display = 'block';
                        arrow.textContent = '▲';
                    } else {
                        content.style.display = 'none';
                        arrow.textContent = '▼';
                    }
                }
            </script>
            
            <div class="subcategories-accordion">
        ''')
        
        html_parts.append('</div>')
        
        return mark_safe(''.join(html_parts))

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
            'assigned_mechanic',    # מכונאי מטפל
        ]
        labels = {
            'bike': 'אופניים',
            'problem_description': 'תיאור התקלה (חופשי)',
            'diagnosis': 'אבחון',
            'assigned_mechanic': 'מכונאי מטפל',
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
    
    # פרטי אופניים
    has_bike = forms.BooleanField(
        label="יש לי אופניים שאני רוצה לרשום עכשיו",
        required=False,
        help_text="אם תסמן, תוכל להוסיף פרטי אופניים כחלק מההרשמה"
    )
    bike_brand = forms.CharField(
        label="יצרן האופניים",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'לדוגמה: Trek, Giant, מרין'})
    )
    bike_model = forms.CharField(
        label="מודל האופניים",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'לדוגמה: FX 3, Talon, אלפין טרייל'})
    )
    bike_color = forms.CharField(
        label="צבע האופניים",
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'לדוגמה: כחול, אדום, שחור'})
    )
    
    # אפשרות לחבר לקוח קיים
    link_existing = forms.BooleanField(
        label="יש לי כבר פרטים במערכת",
        required=False,
        help_text="סמן אם אתה כבר רשום במערכת כלקוח (ע\"י המנהל) ורוצה לחבר את החשבון"
    )

    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password1', 'password2', 
                 'link_existing', 'has_bike', 'bike_brand', 'bike_model', 'bike_color']
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
        has_bike = cleaned_data.get('has_bike')
        bike_brand = cleaned_data.get('bike_brand')
        
        # בדיקת חיבור לקוח קיים
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
        
        # בדיקת פרטי אופניים
        if has_bike and not bike_brand:
            raise forms.ValidationError("אם יש לך אופניים, חובה למלא לפחות את שדה היצרן")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'customer'})
            
            # יצירת או חיבור לקוח
            if hasattr(self, 'existing_customer') and self.cleaned_data.get('link_existing'):
                # עדכון הלקוח הקיים עם המשתמש החדש
                customer = self.existing_customer
                customer.user = user
                # עדכון פרטים אם שונים
                if customer.email != self.cleaned_data['email']:
                    customer.email = self.cleaned_data['email']
                customer.save()
            else:
                # יצירת לקוח חדש
                customer = Customer.objects.create(
                    user=user,
                    name=self.cleaned_data['name'],
                    phone=self.cleaned_data['phone'],
                    email=self.cleaned_data['email'],
                )
            
            # יצירת אופניים אם צוין
            if self.cleaned_data.get('has_bike') and self.cleaned_data.get('bike_brand'):
                Bike.objects.create(
                    customer=customer,
                    brand=self.cleaned_data['bike_brand'],
                    model=self.cleaned_data.get('bike_model', ''),
                    color=self.cleaned_data.get('bike_color', ''),
                )
        return user
    
    
class CustomerRepairJobForm(forms.ModelForm):
    subcategories = forms.ModelMultipleChoiceField(
        queryset=RepairSubCategory.objects.select_related('category').order_by('category__name', 'name'),
        required=False,
        widget=AccordionCheckboxSelectMultiple(),
        label="בחר סוגי התקלות"
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
        widgets = {
            'bike': forms.Select(attrs={
                'class': 'form-select',
                'style': 'width: 100%; padding: 10px; font-size: 16px;'
            }),
            'problem_description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'תאר את התקלה בפירוט... (לדוגמה: השרשרת קופצת, הבלמים חורקים, וכו\')',
                'style': 'width: 100%; padding: 10px; font-size: 16px; resize: vertical;'
            })
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

class RepairDiagnosisForm(forms.ModelForm):
    """טופס לאבחון תיקון על ידי מנהל"""
    class Meta:
        model = RepairJob
        fields = ['diagnosis']
        labels = {
            'diagnosis': 'אבחון והמלצות',
        }
        widgets = {
            'diagnosis': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'תאר את האבחון והפעולות הנדרשות...'
            })
        }


class RepairItemForm(forms.ModelForm):
    """טופס לפעולת תיקון בודדת"""
    class Meta:
        model = RepairItem
        fields = ['description', 'price']
        labels = {
            'description': 'תיאור הפעולה',
            'price': 'מחיר (₪)',
        }
        widgets = {
            'description': forms.TextInput(attrs={
                'placeholder': 'לדוגמה: החלפת בלמים קדמיים'
            }),
            'price': forms.NumberInput(attrs={
                'min': '0',
                'step': '0.01',
                'placeholder': '0.00'
            })
        }


# טופס דינמי לפעולות תיקון מרובות
RepairItemFormSet = forms.modelformset_factory(
    RepairItem,
    form=RepairItemForm,
    extra=1,
    can_delete=True
)


class CustomerApprovalForm(forms.Form):
    """טופס לאישור פעולות על ידי לקוח"""
    def __init__(self, repair_job, data=None, *args, **kwargs):
        super().__init__(data=data, *args, **kwargs)
        self.repair_job = repair_job
        
        # יצירת שדה checkbox לכל פעולה
        repair_items = repair_job.repair_items.all()
        self.fields['approved_items'] = forms.ModelMultipleChoiceField(
            queryset=repair_items,
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label="בחר את הפעולות שברצונך לאשר:",
            initial=repair_items.filter(is_approved_by_customer=True)
        )



class MechanicTaskForm(forms.Form):
    """טופס למכונאי לסימון פעולות שבוצעו עם הערות לכל סעיף"""
    def __init__(self, *args, repair_job=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.repair_job = repair_job
        
        # רק פעולות שאושרו על ידי הלקוח
        approved_items = repair_job.repair_items.filter(is_approved_by_customer=True)
        
        self.fields['completed_items'] = forms.ModelMultipleChoiceField(
            queryset=approved_items.filter(is_completed=False),
            widget=forms.CheckboxSelectMultiple,
            required=False,
            label="בחר את הפעולות שהושלמו:",
        )
        
        # יצירת שדה הערות לכל פעולה
        for item in approved_items:
            field_name = f'notes_{item.id}'
            self.fields[field_name] = forms.CharField(
                label=f"הערות עבור: {item.description}",
                required=False,
                initial=item.notes,
                widget=forms.Textarea(attrs={
                    'rows': 2, 
                    'placeholder': 'למשל: חסר חלק, תקלה נוספת שהתגלתה, עבודה דחופה התקבלה, וכו...'
                }),
                help_text="הערות חשובות - תקועה, הסתייגויות, בעיות שהתגלו, חלקים חסרים, וכו'"
            )
        
        self.fields['general_notes'] = forms.CharField(
            label="הערות כלליות על התיקון",
            required=False,
            widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'הערות כלליות על מצב התיקון...'})
        )


# טופס משולב למנהל - לקוח ואופניים
class CustomerWithBikeForm(forms.Form):
    """טופס למנהל ליצירת/עריכת לקוח עם אופניים בו-זמנית"""
    
    # פרטי לקוח
    customer_name = forms.CharField(label="שם הלקוח", max_length=100)
    customer_phone = forms.CharField(
        label="טלפון",
        max_length=20,
        validators=[RegexValidator(r'^[0-9\-\+]{9,15}$', 'נא להזין מספר טלפון תקין')]
    )
    customer_email = forms.EmailField(label="אימייל", required=False)
    
    # פרטי אופניים
    bike_brand = forms.CharField(label="יצרן האופניים", max_length=50)
    bike_model = forms.CharField(label="מודל האופניים", max_length=50, required=False)
    bike_color = forms.CharField(label="צבע האופניים", max_length=30, required=False)
    
    def __init__(self, *args, **kwargs):
        self.customer_instance = kwargs.pop('customer_instance', None)
        self.bike_instance = kwargs.pop('bike_instance', None)
        super().__init__(*args, **kwargs)
        
        # אם זה עריכה, מילוי הערכים הקיימים
        if self.customer_instance:
            self.fields['customer_name'].initial = self.customer_instance.name
            self.fields['customer_phone'].initial = self.customer_instance.phone
            self.fields['customer_email'].initial = self.customer_instance.email
            
        if self.bike_instance:
            self.fields['bike_brand'].initial = self.bike_instance.brand
            self.fields['bike_model'].initial = self.bike_instance.model
            self.fields['bike_color'].initial = self.bike_instance.color
    
    def save(self):
        """שמירת הלקוח והאופניים"""
        
        # יצירת או עדכון לקוח
        if self.customer_instance:
            customer = self.customer_instance
            customer.name = self.cleaned_data['customer_name']
            customer.phone = self.cleaned_data['customer_phone']
            customer.email = self.cleaned_data['customer_email']
            customer.save()
        else:
            customer = Customer.objects.create(
                name=self.cleaned_data['customer_name'],
                phone=self.cleaned_data['customer_phone'],
                email=self.cleaned_data['customer_email'],
                user=None  # נוצר ע"י מנהל
            )
        
        # יצירת או עדכון אופניים
        if self.bike_instance:
            bike = self.bike_instance
            bike.customer = customer
            bike.brand = self.cleaned_data['bike_brand']
            bike.model = self.cleaned_data['bike_model']
            bike.color = self.cleaned_data['bike_color']
            bike.save()
        else:
            bike = Bike.objects.create(
                customer=customer,
                brand=self.cleaned_data['bike_brand'],
                model=self.cleaned_data['bike_model'],
                color=self.cleaned_data['bike_color'],
            )
        
        return customer, bike

# טופס לקוח להוספת אופניים נוספות
class CustomerAddBikeForm(forms.ModelForm):
    """טופס ללקוח להוספת אופניים נוספות לחשבון שלו"""
    
    class Meta:
        model = Bike
        fields = ['brand', 'model', 'color']
        labels = {
            'brand': 'יצרן האופניים',
            'model': 'מודל (לא חובה)',
            'color': 'צבע (לא חובה)',
        }
        widgets = {
            'brand': forms.TextInput(attrs={'placeholder': 'לדוגמה: Trek, Giant, מרין'}),
            'model': forms.TextInput(attrs={'placeholder': 'לדוגמה: FX 3, Talon, אלפין טרייל'}),
            'color': forms.TextInput(attrs={'placeholder': 'לדוגמה: כחול, אדום, שחור'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        bike = super().save(commit=False)
        if self.customer:
            bike.customer = self.customer
        if commit:
            bike.save()
        return bike

class AccordionCheckboxSelectMultiple(CheckboxSelectMultiple):
    """Widget שמציג תתי קטגוריות באקורדיון מאורגן לפי קטגוריות"""
    
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []
        
        # קבלת כל התתי קטגוריות מאורגנות לפי קטגוריה
        categories = {}
        for choice in self.choices:
            choice_value, choice_label = choice
            # פירוק התווית לקטגוריה ותת קטגוריה
            if ' > ' in choice_label:
                category_name, subcategory_name = choice_label.split(' > ', 1)
            else:
                category_name, subcategory_name = 'כללי', choice_label
            
            if category_name not in categories:
                categories[category_name] = []
            
            categories[category_name].append({
                'value': choice_value,
                'label': subcategory_name,
                'checked': choice_value in value
            })
        
        # בניית HTML לאקורדיון
        html_parts = []
        
        for category_name, subcategories in categories.items():
            category_id = f"category_{category_name.replace(' ', '_')}"
            
            # כותרת קטגוריה
            html_parts.append(f'''
                <div class="accordion-category">
                    <div class="accordion-header" onclick="toggleCategory('{category_id}')">
                        <span class="category-name">{category_name}</span>
                        <span class="accordion-arrow" id="arrow_{category_id}">▼</span>
                    </div>
                    <div class="accordion-content" id="{category_id}" style="display: none;">
            ''')
            
            # תתי קטגוריות
            for subcategory in subcategories:
                checked = 'checked' if subcategory['checked'] else ''
                html_parts.append(f'''
                    <div class="subcategory-item">
                        <label>
                            <input type="checkbox" name="{name}" value="{subcategory['value']}" {checked}>
                            <span class="subcategory-label">{subcategory['label']}</span>
                        </label>
                    </div>
                ''')
            
            html_parts.append('</div></div>')
        
        # הוספת CSS ו-JavaScript לאקורדיון
        html_parts.insert(0, '''
            <style>
                .accordion-category {
                    margin-bottom: 10px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    overflow: hidden;
                }
                
                .accordion-header {
                    background-color: #007bff;
                    color: white;
                    padding: 12px 15px;
                    cursor: pointer;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-weight: bold;
                }
                
                .accordion-header:hover {
                    background-color: #0056b3;
                }
                
                .accordion-content {
                    background-color: #f8f9fa;
                    padding: 10px;
                }
                
                .subcategory-item {
                    padding: 8px 0;
                    border-bottom: 1px solid #e9ecef;
                }
                
                .subcategory-item:last-child {
                    border-bottom: none;
                }
                
                .subcategory-item label {
                    display: flex;
                    align-items: center;
                    cursor: pointer;
                    margin: 0;
                }
                
                .subcategory-item input[type="checkbox"] {
                    margin-left: 10px;
                    margin-right: 0;
                    transform: scale(1.2);
                }
                
                .subcategory-label {
                    flex-grow: 1;
                    padding-right: 10px;
                }
                
                @media (max-width: 768px) {
                    .accordion-header {
                        font-size: 14px;
                        padding: 10px 12px;
                    }
                    
                    .subcategory-item input[type="checkbox"] {
                        transform: scale(1.3);
                        margin-left: 12px;
                    }
                }
            </style>
            
            <script>
                function toggleCategory(categoryId) {
                    const content = document.getElementById(categoryId);
                    const arrow = document.getElementById('arrow_' + categoryId);
                    
                    if (content.style.display === 'none') {
                        content.style.display = 'block';
                        arrow.textContent = '▲';
                    } else {
                        content.style.display = 'none';
                        arrow.textContent = '▼';
                    }
                }
            </script>
            
            <div class="subcategories-accordion">
        ''')
        
        html_parts.append('</div>')

