from django import forms
from .models import Customer
from .models import Bike
from .models import RepairJob

class RepairJobForm(forms.ModelForm):
    class Meta:
        model = RepairJob
        fields = ['bike', 'problem_types', 'problem_description', 'diagnosis', 'quote_price', 'is_approved']
        labels = {
            'bike': 'אופניים',
            'problem_types': 'תקלות',
            'problem_description': 'תיאור התקלה',
            'diagnosis': 'אבחון',
            'quote_price': 'הצעת מחיר',
            'is_approved': 'אושר על ידי הלקוח'
        }
        widgets = {
            'problem_types': forms.CheckboxSelectMultiple
        }



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email']
        labels = {
            'name': 'שם',
            'phone': 'טלפון',
            'email': 'אימייל (לא חובה)'
        }
        
class BikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ['customer', 'brand', 'model', 'color']
        labels = {
            'customer': 'לקוח',
            'brand': 'יצרן',
            'model': 'מודל',
            'color': 'צבע'
        }
