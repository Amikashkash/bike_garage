from django.contrib.auth.decorators import user_passes_test

def role_required(allowed_roles):
    def check(user):
        # שדרוג: לאפשר גם superuser אוטומטית
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return hasattr(user, 'userprofile') and user.userprofile.role in allowed_roles
    return user_passes_test(check)

# קיצורי דרך
customer_required = role_required(['customer'])
mechanic_required = role_required(['mechanic'])
manager_required = role_required(['manager'])
staff_required   = role_required(['mechanic', 'manager'])
