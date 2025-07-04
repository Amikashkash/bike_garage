from django.contrib.auth.decorators import user_passes_test

def role_required(allowed_roles):
    """
    Decorator that allows access only to users with a role listed in allowed_roles.
    Roles are defined in UserProfile.role.
    """
    def check(user):
        if not user.is_authenticated:
            return False
        return hasattr(user, 'userprofile') and user.userprofile.role in allowed_roles
    return user_passes_test(check)

# קיצורי דרך שימושיים לפי תפקידים
customer_required = role_required(['customer'])
mechanic_required = role_required(['mechanic'])
manager_required = role_required(['manager'])
staff_required = role_required(['mechanic', 'manager'])  # כל מי שצוות המוסך
