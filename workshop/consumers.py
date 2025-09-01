import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import UserProfile, Customer

logger = logging.getLogger(__name__)


class WorkshopConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.user_type = self.scope['url_route']['kwargs']['user_type']
        
        # Only allow authenticated users
        if not self.user.is_authenticated:
            await self.close()
            return
            
        # Get user profile to determine role
        self.user_profile = await self.get_user_profile()
        if not self.user_profile:
            await self.close()
            return
            
        # Validate user_type matches their role
        if not await self.validate_user_type():
            await self.close()
            return
            
        # Join appropriate groups based on user type
        await self.join_user_groups()
        
        await self.accept()
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'מחובר כ{self.get_role_display()}',
            'user_type': self.user_type,
            'user_id': self.user.id
        }))

    async def disconnect(self, close_code):
        # Leave all groups
        if hasattr(self, 'groups_joined'):
            for group in self.groups_joined:
                await self.channel_layer.group_discard(group, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # Handle different message types
            if message_type == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': data.get('timestamp')
                }))
            elif message_type == 'mark_notification_read':
                await self.handle_mark_notification_read(data)
            else:
                # Handle other message types based on user role
                await self.handle_role_specific_message(data)
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'פורמט הודעה לא תקין'
            }))

    # Group message handlers
    async def repair_status_update(self, event):
        """Handle repair status updates"""
        await self.send(text_data=json.dumps({
            'type': 'repair_status_update',
            'repair_id': event['repair_id'],
            'status': event['status'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    async def new_repair_assignment(self, event):
        """Handle new repair assignments for mechanics"""
        await self.send(text_data=json.dumps({
            'type': 'new_repair_assignment',
            'repair_id': event['repair_id'],
            'bike_info': event['bike_info'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    async def mechanic_stuck_notification(self, event):
        """Handle mechanic stuck notifications for managers"""
        await self.send(text_data=json.dumps({
            'type': 'mechanic_stuck_notification',
            'repair_id': event['repair_id'],
            'mechanic_name': event['mechanic_name'],
            'reason': event['reason'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    async def customer_notification(self, event):
        """Handle customer notifications"""
        await self.send(text_data=json.dumps({
            'type': 'customer_notification',
            'notification_id': event['notification_id'],
            'title': event['title'],
            'message': event['message'],
            'notification_type': event['notification_type'],
            'action_url': event.get('action_url', ''),
            'timestamp': event['timestamp']
        }))

    async def quality_check_ready(self, event):
        """Handle quality check ready notifications for managers"""
        await self.send(text_data=json.dumps({
            'type': 'quality_check_ready',
            'repair_id': event['repair_id'],
            'bike_info': event['bike_info'],
            'mechanic_name': event['mechanic_name'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    # Helper methods
    @database_sync_to_async
    def get_user_profile(self):
        try:
            return UserProfile.objects.get(user=self.user)
        except UserProfile.DoesNotExist:
            return None

    @database_sync_to_async
    def validate_user_type(self):
        """Validate that user_type matches user's actual role"""
        valid_types = {
            'customer': 'customer',
            'mechanic': 'mechanic', 
            'manager': 'manager'
        }
        
        if self.user_type not in valid_types:
            return False
            
        return self.user_profile.role == valid_types[self.user_type]

    async def new_repair_created(self, event):
        """Handle new repair created notification"""
        # Log for debugging
        logger.info(f"New repair created notification: {event}")
        
        # Send to client
        await self.send(text_data=json.dumps({
            'type': 'new_repair_created',
            'repair_id': event['repair_id'],
            'customer_name': event['customer_name'],
            'bike_info': event['bike_info'], 
            'problem_description': event['problem_description'],
            'status': event.get('status', 'pending_diagnosis'),
            'message': event['message']
        }))
        

    async def join_user_groups(self):
        """Join appropriate WebSocket groups based on user type"""
        self.groups_joined = []
        
        if self.user_type == 'customer':
            # Join customer-specific group
            customer_group = f"customer_{self.user.id}"
            await self.channel_layer.group_add(customer_group, self.channel_name)
            self.groups_joined.append(customer_group)
            
            # Join general customer notifications group
            await self.channel_layer.group_add("customers", self.channel_name)
            self.groups_joined.append("customers")
            
        elif self.user_type == 'mechanic':
            # Join mechanic-specific group
            mechanic_group = f"mechanic_{self.user.id}"
            await self.channel_layer.group_add(mechanic_group, self.channel_name)
            self.groups_joined.append(mechanic_group)
            
            # Join general mechanics group
            await self.channel_layer.group_add("mechanics", self.channel_name)
            self.groups_joined.append("mechanics")
            
        elif self.user_type == 'manager':
            # Join manager-specific group
            manager_group = f"manager_{self.user.id}"
            await self.channel_layer.group_add(manager_group, self.channel_name)
            self.groups_joined.append(manager_group)
            
            # Join managers group for stuck repairs and quality checks
            await self.channel_layer.group_add("managers", self.channel_name)
            self.groups_joined.append("managers")
            
            # Managers also get mechanic notifications
            await self.channel_layer.group_add("mechanics", self.channel_name)
            self.groups_joined.append("mechanics")

    def get_role_display(self):
        """Get Hebrew role display"""
        role_display = {
            'customer': 'לקוח',
            'mechanic': 'מכונאי', 
            'manager': 'מנהל'
        }
        return role_display.get(self.user_type, 'משתמש')

    async def handle_mark_notification_read(self, data):
        """Handle marking notifications as read"""
        notification_id = data.get('notification_id')
        if notification_id:
            await self.mark_notification_read(notification_id)

    @database_sync_to_async 
    def mark_notification_read(self, notification_id):
        """Mark customer notification as read"""
        from .models import CustomerNotification
        try:
            if self.user_type == 'customer':
                # Get customer profile
                customer = Customer.objects.get(user=self.user)
                notification = CustomerNotification.objects.get(
                    id=notification_id, 
                    customer=customer
                )
                notification.mark_as_read()
        except (Customer.DoesNotExist, CustomerNotification.DoesNotExist):
            pass

    async def handle_role_specific_message(self, data):
        """Handle messages specific to user roles"""
        message_type = data.get('type')
        
        if self.user_type == 'mechanic':
            if message_type == 'complete_repair_item':
                await self.handle_complete_repair_item(data)
            elif message_type == 'mark_stuck':
                await self.handle_mark_stuck(data)
                
        elif self.user_type == 'manager':
            if message_type == 'approve_quality':
                await self.handle_approve_quality(data)
            elif message_type == 'resolve_stuck_repair':
                await self.handle_resolve_stuck_repair(data)

    async def handle_complete_repair_item(self, data):
        """Handle mechanic completing a repair item"""
        # This will be implemented in Phase 5
        pass

    async def handle_mark_stuck(self, data):
        """Handle mechanic marking repair as stuck"""
        # This will be implemented in Phase 5
        pass

    async def handle_approve_quality(self, data):
        """Handle manager approving quality check"""
        # This will be implemented in Phase 5
        pass

    async def handle_resolve_stuck_repair(self, data):
        """Handle manager resolving stuck repair"""
        # This will be implemented in Phase 5
        pass