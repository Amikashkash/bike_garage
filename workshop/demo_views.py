"""
Simple test page for demonstrating push notifications
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Customer, RepairJob
from .notification_service import NotificationService

def notification_demo(request):
    """Demo page for testing notifications"""
    customers = Customer.objects.all()[:5]  # Get first 5 customers
    
    context = {
        'customers': customers,
        'title': 'בדיקת מערכת התראות'
    }
    
    return render(request, 'workshop/notification_demo.html', context)


@csrf_exempt
def send_demo_notification(request):
    """Send a demo notification for testing"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            customer_id = data.get('customer_id')
            notification_type = data.get('type', 'repair_update')
            
            customer = Customer.objects.get(id=customer_id)
            
            # Create different types of test notifications
            if notification_type == 'approval_needed':
                # Mock a repair job for testing
                repair_job = RepairJob.objects.filter(bike__customer=customer).first()
                if repair_job:
                    notification = NotificationService.notify_approval_needed(repair_job)
                else:
                    notification = NotificationService.create_notification(
                        customer=customer,
                        notification_type='approval_needed',
                        title='נדרש אישור - תיקון בדיקה',
                        message='זוהי הודעת בדיקה לאישור תיקון. לחץ כאן לצפייה בפרטים.',
                        action_url='/'
                    )
            
            elif notification_type == 'ready_for_pickup':
                notification = NotificationService.create_notification(
                    customer=customer,
                    notification_type='ready_for_pickup',
                    title='האופניים מוכנים לאיסוף! 🚴‍♂️',
                    message='התיקון הושלם בהצלחה! אנא הגע למוסך לקחת את האופניים.',
                    action_url='/'
                )
            
            else:  # repair_update
                notification = NotificationService.create_notification(
                    customer=customer,
                    notification_type='repair_update',
                    title='עדכון תיקון 🔧',
                    message='יש עדכון חדש על התיקון שלך. לחץ לצפייה בפרטים.',
                    action_url='/'
                )
            
            return JsonResponse({
                'success': True,
                'message': f'התראה נשלחה ללקוח {customer.name}',
                'notification_id': notification.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'})
