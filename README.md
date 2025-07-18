# 🚲 Bike Garage Management System

A comprehensive Django-based management system for bicycle repair shops, featuring customer management, repair tracking, quality control, and mechanic workflow management.

## Features

### � Core Functionality
- **Customer Management**: Full customer database with contact information and repair history
- **Repair Job Tracking**: Complete workflow from initial report to customer pickup
- **Inventory Management**: Track repair items, parts, and pricing
- **Mechanic Assignment**: Assign repairs to mechanics and track progress
- **Quality Control**: Built-in quality assurance process with manager approval
- **Stuck Job Management**: Handle blocked repairs with manager intervention

### 📊 Dashboard Views
- **Manager Dashboard**: Overview of all operations, stuck jobs, and quality control
- **Mechanic Dashboard**: Personal task list and repair completion tools
- **Customer Portal**: Check repair status and approve estimates

### 🎯 Advanced Features
- **Multi-status Workflow**: Detailed tracking from diagnosis to delivery
- **Progress Calculation**: Real-time progress tracking for each repair
- **Quality Assurance**: Mandatory quality checks before customer pickup
- **Notification System**: Automated customer notifications
- **Responsive Design**: Mobile-friendly interface for on-the-go access

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Frontend**: Bootstrap 5, jQuery 3.6.0
- **Deployment**: Render.com
- **Language**: Python 3.11+

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/bike-garage.git
   cd bike-garage
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

5. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to access the application.

## Usage

### User Roles

1. **Manager**
   - Access to all features
   - Can create and assign repairs
   - Quality control approval
   - System configuration

2. **Mechanic**
   - View assigned repairs
   - Update repair progress
   - Mark items as completed or blocked
   - Request manager assistance

3. **Customer**
   - View repair status
   - Approve estimates
   - Receive notifications

### Workflow

1. **Report Issue**: Customer reports a problem
2. **Diagnosis**: Manager diagnoses and creates repair estimate
3. **Approval**: Customer approves repair items
4. **Assignment**: Manager assigns repair to mechanic
5. **Execution**: Mechanic performs repairs
6. **Quality Check**: Manager reviews completed work
7. **Pickup**: Customer is notified and picks up bicycle

## Database Schema

### Main Models

- **Customer**: Customer information and contact details
- **Bike**: Bicycle information linked to customers
- **RepairJob**: Main repair tracking entity
- **RepairItem**: Individual repair tasks and items
- **UserProfile**: Extended user information with roles

### Key Fields

- **RepairJob Status**: `reported`, `diagnosed`, `approved`, `in_progress`, `awaiting_quality_check`, `quality_approved`, `completed`, `delivered`
- **RepairItem Status**: `pending`, `completed`, `blocked`
- **Quality Fields**: `quality_checked_by`, `quality_check_date`, `quality_notes`
- **Stuck Job Fields**: `is_stuck`, `stuck_reason`, `manager_response`

## Deployment

### Production Deployment (Render.com)

1. **Prepare environment variables**
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://...
   ALLOWED_HOSTS=your-domain.com
   ```

2. **Deploy to Render**
   - Connect your GitHub repository
   - Set environment variables
   - Deploy with build command: `pip install -r requirements.txt`
   - Start command: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn garage.wsgi:application`

### Environment Variables

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

## Changelog

### Version 2.0.0 (July 2025)
- Added quality control system
- Implemented stuck job management
- Enhanced repair item tracking
- Improved dashboard functionality
- Fixed JavaScript loading issues
- Added comprehensive notification system

### Version 1.0.0 (Initial Release)
- Basic repair tracking
- Customer management
- Mechanic assignment
- Simple dashboard interface
| מנהל | admin | admin123 | גישה מלאה + ממשק ניהול |
| מכונאי | mechanic | mech123 | ניהול תיקונים ולקוחות |
| לקוח | customer | cust123 | דיווח תקלות |

## מבנה הפרויקט

```
bikegarage/
├── garage/                    # הגדרות פרויקט
│   ├── settings.py           # הגדרות Django
│   ├── urls.py              # URLs ראשיים
│   └── wsgi.py              # הגדרות שרת
├── workshop/                 # אפליקציה עיקרית
│   ├── models.py            # מודלים של בסיס הנתונים
│   ├── views.py             # לוגיקה עיסקית
│   ├── forms.py             # טפסים
│   ├── urls.py              # URLs של האפליקציה
│   ├── admin.py             # הגדרות ממשק ניהול
│   ├── permissions.py       # הגדרות הרשאות
│   ├── templates/           # תבניות HTML
│   └── management/          # פקודות ניהול מותאמות
├── db.sqlite3               # בסיס נתונים
└── manage.py               # כלי ניהול Django
```

## מודלים עיקריים

### UserProfile
- קישור משתמש Django לתפקיד במערכת
- תפקידים: customer, mechanic, manager

### Customer
- פרטי לקוח: שם, טלפון, אימייל
- קישור למשתמש Django (אופציונלי)

### Bike
- פרטי אופניים: יצרן, מודל, צבע
- שייכות ללקוח

### RepairCategory & RepairSubCategory
- מערכת היררכית לסיווג תקלות
- דוגמאות: בלמים > החלפת גומיות בלם

### RepairJob
- תיק תיקון: אופניים, תקלות, תיאור, אבחון
- מחיר מוערך ואישור לקוח

## תכונות מתקדמות

### מערכת הרשאות
- דקורטורים מותאמים להגבלת גישה
- הפרדה בין תפקידים שונים
- בדיקת הרשאות ברמת הצג (view)

### ממשק ניהול מותאם
- הצגה מותאמת לכל מודל
- חיפוש וסינון
- קישורים בין מודלים

### תבניות רספונסיביות
- עיצוב מותאם לעברית (RTL)
- תפריט דינמי לפי הרשאות
- הודעות משתמש

## פיתוח נוסף

### הוספת תכונות חדשות
1. צור מודל חדש ב-`models.py`
2. הוסף טופס ב-`forms.py`
3. צור view ב-`views.py`
4. הוסף URL ב-`urls.py`
5. צור תבנית HTML
6. הרץ `makemigrations` ו-`migrate`

### בדיקות
```bash
python manage.py test
```

### איסוף קבצים סטטיים לפרודקשן
```bash
python manage.py collectstatic
```

## תמיכה

לשאלות ובעיות, פנה למפתח הפרויקט או צור issue בגיטהאב.
## ⭐ עדכון חדש: טופס אישור לקוח מתקדם

### 🎯 תכונה חדשה - אישור סלקטיבי של פעולות תיקון

הלקוח כעת יכול לבחור בדיוק אילו פעולות תיקון הוא מאשר:

#### ✅ מה עובד:
- **בחירה אינדיבידואלית** של כל פעולת תיקון
- **חישוב מחיר דינמי** בזמן אמת
- **ממשק ידידותי** עם תיבות סימון
- **אישורים חלקיים** - לא חובה לאשר הכל
- **עדכון סטטוס אוטומטי** של התיקון

#### 🔗 כיצד לבדוק:
1. התחבר כלקוח: `customer_test` / `test123456`
2. גש לכתובת: http://localhost:8000/repair/5/approve/
3. בחר פעולות תיקון ספציפיות
4. לחץ "אשר פעולות נבחרות"

#### 🧪 נתוני בדיקה:
```bash
python manage.py create_test_approval
```
יוצר תיקון עם 5 פעולות שונות לבדיקת הטופס.

---

© 2025 מוסך האופניים - Django Project
