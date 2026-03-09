from core.models import Membership

def get_user_role(user, organization):
    membership = Membership.objects.filter(
        user=user,
        organization=organization
    ).first()

    return membership.role if membership else None
