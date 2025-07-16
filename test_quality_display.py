import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'garage.settings')

# Setup Django
django.setup()

from workshop.models import RepairJob, User

def test_quality_display():
    print("🔍 בדיקת תצוגת בקרת איכות...")
    
    # בדיקה - האם יש תיקון שמוכן לבדיקת איכות
    awaiting_quality = RepairJob.objects.filter(status='awaiting_quality_check')
    print(f"\n📋 תיקונים שממתינים לבדיקת איכות: {awaiting_quality.count()}")
    
    for job in awaiting_quality:
        print(f"   - תיקון #{job.id} של {job.bike.customer.name} - {job.bike}")
        print(f"     סטטוס: {job.status}")
        print(f"     אבחון קיים: {bool(job.diagnosis)}")
        print(f"     עבודה הושלמה: {hasattr(job, 'work_completed') and bool(job.work_completed)}")
    
    # בדיקה - איך נראה הדשבורד
    all_jobs = RepairJob.objects.all()
    print(f"\n📊 סה\"כ תיקונים במערכת: {all_jobs.count()}")
    
    status_counts = {}
    for job in all_jobs:
        status = job.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\n📈 פילוח לפי סטטוסים:")
    for status, count in status_counts.items():
        print(f"   - {status}: {count}")
    
    # נבדוק את המנהל
    try:
        manager = User.objects.filter(role='manager').first()
        if manager:
            print(f"\n👨‍💼 מנהל קיים: {manager.username}")
        else:
            print("\n⚠️ לא נמצא מנהל במערכת")
    except Exception as e:
        print(f"\n❌ שגיאה בבדיקת מנהל: {e}")
    
    # בוא נבדוק אם יש תיקונים שמוכנים לסיום
    completed_jobs = RepairJob.objects.filter(status='work_completed')
    print(f"\n🔧 תיקונים שמסומנים כ-work_completed: {completed_jobs.count()}")
    
    # בוא נבדוק כל תיקון ונראה מה הסטטוס שלו
    print("\n📄 כל התיקונים במערכת:")
    for job in all_jobs.order_by('-created_at')[:10]:  # 10 האחרונים
        print(f"   #{job.id}: {job.bike.customer.name} - {job.status}")
        if hasattr(job, 'work_completed') and hasattr(job, 'work_completed') and job.work_completed:
            print(f"      עבודה הושלמה: {str(job.work_completed)[:50]}...")
        if hasattr(job, 'diagnosis') and job.diagnosis:
            print(f"      אבחון: {job.diagnosis[:50]}...")
    
    return awaiting_quality.count() > 0

if __name__ == "__main__":
    has_quality_items = test_quality_display()
    
    if not has_quality_items:
        print("\n🎯 נדרש ליצור תיקון לבדיקה...")
        
        # ניצור תיקון שמוכן לבדיקת איכות
        from workshop.models import User
        
        # נמצא או ניצור מכונאי
        mechanic = User.objects.filter(role='mechanic').first()
        if not mechanic:
            print("יוצר מכונאי...")
            mechanic = User.objects.create_user(
                username='mechanic_test',
                password='test123',
                first_name='מכונאי',
                last_name='בדיקה',
                role='mechanic'
            )
        
        # ניצור תיקון חדש
        from workshop.models import Customer, Bike
        
        # ניצור לקוח
        customer = Customer.objects.create(
            name='לקוח בדיקה',
            phone='050-1234567',
            email='test@example.com'
        )
        
        # ניצור אופניים
        bike = Bike.objects.create(
            customer=customer,
            brand='Trek',
            model='Mountain',
            color='שחור'
        )
        
        job = RepairJob.objects.create(
            bike=bike,
            problem_description='בעיה בבלמים',
            status='awaiting_quality_check',
            diagnosis='בלמים זקוקים להחלפה',
            assigned_mechanic=mechanic
        )
        
        print(f"✅ נוצר תיקון #{job.id} לבדיקת איכות")
    else:
        print("\n✅ יש תיקונים שממתינים לבדיקת איכות!")
