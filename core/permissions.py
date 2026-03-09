from core.models import Membership


def get_membership(user, organization):
    return Membership.objects.filter(
        user=user,
        organization=organization
    ).first()


def is_admin(user, organization):
    membership = get_membership(user, organization)
    return membership and membership.role == "admin"


from core.models import Membership

def is_manager(user, organization):
    if not user.is_authenticated:
        return False

    return Membership.objects.filter(
        user=user,
        organization=organization,
        role__in=["admin", "manager"]
    ).exists()



def is_member(user, organization):
    return Membership.objects.filter(
        user=user,
        organization=organization
    ).exists()
