from django.core.management.base import BaseCommand
from workshop.models import Customer, Bike, RepairJob, RepairItem
from django.contrib.auth.models import User
from workshop.models import UserProfile

class Command(BaseCommand):
    help = 'יצירת נתונים לבדיקת טופס אישור לקוח'

    def handle(self, *args, **options):
        # יצירת לקוח עם משתמש
        customer_user, created = User.objects.get_or_create(
            username='customer_test',
            defaults={
                'first_name': 'לקוח',
                'last_name': 'בדיקה',
                'email': 'customer@test.com'
            }
        )
        if created:
            customer_user.set_password('test123456')
            customer_user.save()
            UserProfile.objects.get_or_create(
                user=customer_user,
                defaults={'role': 'customer'}
            )
            self.stdout.write('נוצר משתמש לקוח: customer_test / test123456')
        
        customer, created = Customer.objects.get_or_create(
            user=customer_user,
            defaults={
                'name': 'לקוח בדיקה',
                'phone': '050-1234567',
                'email': 'customer@test.com'
            }
        )
        if created:
            self.stdout.write('נוצר לקוח חדש')
        
        # יצירת אופניים
        bike, created = Bike.objects.get_or_create(
            customer=customer,
            brand='Trek',
            defaults={
                'model': 'FX 3',
                'color': 'כחול'
            }
        )
        if created:
            self.stdout.write('נוצרו אופניים חדשות')
        
        # יצירת תיקון
        repair_job, created = RepairJob.objects.get_or_create(
            bike=bike,
            problem_description='בלמים לא עובדים טוב',
            defaults={
                'status': 'diagnosed',
                'diagnosis': 'נדרש החלפת בלמים קדמיים ואחוריים, ניקוי שרשרת וכוונון הילוכים'
            }
        )
        if created:
            self.stdout.write('נוצר תיקון חדש')
        
        # יצירת פריטי תיקון
        items_data = [
            ('החלפת בלמים קדמיים', 150.00, 'כולל רפידות חדשות'),
            ('החלפת בלמים אחוריים', 120.00, 'כולל רפידות חדשות'),
            ('ניקוי ושמן שרשרת', 50.00, ''),
            ('כוונון הילוכים', 80.00, 'כוונון מלא של כל ההילוכים'),
            ('בדיקת גלגלים ומתיחת חישורים', 60.00, ''),
        ]
        
        for description, price, notes in items_data:
            item, created = RepairItem.objects.get_or_create(
                repair_job=repair_job,
                description=description,
                defaults={
                    'price': price,
                    'notes': notes
                }
            )
            if created:
                self.stdout.write(f'נוצר פריט: {description}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ נוצרו נתונים לבדיקה!\n'
                f'🔗 עבור לכתובת: /repair/{repair_job.id}/approve/\n'
                f'👤 התחבר עם: customer_test / test123456'
            )
        )
