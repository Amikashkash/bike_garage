from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from workshop.models import UserProfile, Customer, RepairCategory, RepairSubCategory

class Command(BaseCommand):
    help = 'יצירת נתונים בסיסיים לפרויקט'

    def handle(self, *args, **options):
        # יצירת קטגוריות תיקון בסיסיות
        categories_data = [
            {
                'name': 'בלמים',
                'subcategories': ['החלפת גומיות בלם', 'כיוון בלמים', 'החלפת כבלי בלם']
            },
            {
                'name': 'גלגלים',
                'subcategories': ['תיקון פנצ\'ר', 'החלפת שפיצים', 'מרכוז גלגל']
            },
            {
                'name': 'שלדה',
                'subcategories': ['ריתוך', 'צביעה', 'החלפת רכיבים']
            },
            {
                'name': 'הילוכים',
                'subcategories': ['כיוון הילוכים', 'החלפת שרשרת', 'החלפת גלגלי שיניים']
            }
        ]

        for cat_data in categories_data:
            category, created = RepairCategory.objects.get_or_create(
                name=cat_data['name']
            )
            if created:
                self.stdout.write(f'נוצרה קטגוריה: {category.name}')
            
            for sub_name in cat_data['subcategories']:
                subcategory, created = RepairSubCategory.objects.get_or_create(
                    category=category,
                    name=sub_name
                )
                if created:
                    self.stdout.write(f'  נוצרה תת-קטגוריה: {subcategory.name}')

        # יצירת משתמש מנהל בסיסי אם לא קיים
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='admin123'
            )
            UserProfile.objects.get_or_create(user=admin_user, defaults={'role': 'manager'})
            self.stdout.write('נוצר משתמש מנהל: admin/admin123')
        else:
            admin_user = User.objects.get(username='admin')
            UserProfile.objects.get_or_create(user=admin_user, defaults={'role': 'manager'})

        # יצירת משתמש מכונאי לדוגמה
        if not User.objects.filter(username='mechanic').exists():
            mechanic_user = User.objects.create_user(
                username='mechanic',
                email='mechanic@test.com',
                password='mech123'
            )
            UserProfile.objects.get_or_create(user=mechanic_user, defaults={'role': 'mechanic'})
            self.stdout.write('נוצר משתמש מכונאי: mechanic/mech123')
        else:
            mechanic_user = User.objects.get(username='mechanic')
            UserProfile.objects.get_or_create(user=mechanic_user, defaults={'role': 'mechanic'})

        # יצירת לקוח לדוגמה
        if not User.objects.filter(username='customer').exists():
            customer_user = User.objects.create_user(
                username='customer',
                email='customer@test.com',
                password='cust123'
            )
            UserProfile.objects.get_or_create(user=customer_user, defaults={'role': 'customer'})
            Customer.objects.get_or_create(
                user=customer_user,
                defaults={
                    'name': 'לקוח לדוגמה',
                    'phone': '050-1234567',
                    'email': 'customer@test.com'
                }
            )
            self.stdout.write('נוצר לקוח לדוגמה: customer/cust123')
        else:
            customer_user = User.objects.get(username='customer')
            UserProfile.objects.get_or_create(user=customer_user, defaults={'role': 'customer'})

        self.stdout.write(self.style.SUCCESS('הנתונים הבסיסיים נוצרו בהצלחה!'))
