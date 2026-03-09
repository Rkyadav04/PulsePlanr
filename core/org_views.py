from time import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from urllib3 import request
from core.models import Organization, Membership, User
from core.forms import EmailInviteForm
from core.invite_models import OrganizationInvite
from django.urls import reverse
from django.contrib import messages
from core.permissions import is_manager
from core.permissions import is_admin
from core.utils import get_user_role

@login_required
def create_organization(request):
    if request.method == "POST":
        name = request.POST.get("name")
        desc = request.POST.get("description")
        org = Organization.objects.create(name=name, description=desc)

        # Add current user as admin
        Membership.objects.create(
            user=request.user,
            organization=org,
            role='admin'
        )
        return redirect("org_dashboard", org_id=org.id)

    return render(request, "organization/create_org.html")


@login_required
def org_dashboard(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)

    role = get_user_role(request.user, organization)

    if not role:
        return redirect("dashboard")

    context = {
        "organization": organization,
        "role": role,
    }

    return render(request, "organization/org_dashboard.html", context)

   

@login_required
def invite_member(request, org_id):
    org = get_object_or_404(Organization, id=org_id)

    if not is_manager(request.user, org):
        messages.error(request, "You do not have permission to invite members.")
        return redirect("org_dashboard", org_id=org.id)

    if request.method == "POST":
        form = EmailInviteForm(request.POST)
        if form.is_valid():
            invite = OrganizationInvite.objects.create(
                email=form.cleaned_data["email"],
                role=form.cleaned_data["role"],
                organization=org,
                invited_by=request.user,
            )

            invite_link = request.build_absolute_uri(
                reverse("register") + f"?invite={invite.token}"
            )

            send_mail(
                subject=f"You’re invited to join {org.name}",
                message=f"""
Hello,

You have been invited to join {org.name} on PulsePlanr.

Register here:
{invite_link}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[invite.email],
                fail_silently=False,
            )

            messages.success(request, "Invitation sent successfully.")
            return redirect("org_dashboard", org.id)
    else:
        form = EmailInviteForm()

    return render(
        request,
        "organization/invite_member.html",
        {
            "organization": org,
            "form": form,
        }
    )


@login_required(login_url="login")
def accept_invite(request, token):
    invite = get_object_or_404(OrganizationInvite, token=token, accepted=False)
     # Email must match logged-in user
    if invite.email.lower() != request.user.email.lower():
        messages.error(
            request,
            "This invitation was sent to a different email address."
        )
        return redirect("dashboard")

    # Expiration check
    if invite.expires_at and invite.expires_at < timezone.now():
        messages.error(request, "This invitation has expired.")
        return redirect("dashboard")

    # Avoid duplicate memberships
    membership_exists = Membership.objects.filter(
        user=request.user,
        organization=invite.organization
    ).exists()

    if not membership_exists:
        Membership.objects.create(
            user=request.user,
            organization=invite.organization,
            role=invite.role
        )
        messages.success(
            request,
            f"You have joined {invite.organization.name}."
        )
    else:
        messages.info(
            request,
            "You are already a member of this organization."
        )

    # Mark invite as accepted
    invite.accepted = True
    invite.save(update_fields=["accepted"])

    return redirect("org_dashboard", org_id=invite.organization.id)



@login_required
def remove_member(request, org_id, user_id):
    org = get_object_or_404(Organization, id=org_id)

    if not is_admin(request.user, org):
        messages.error(request, "Only admins can remove members.")
        return redirect("org_dashboard", org_id=org.id)

    Membership.objects.filter(
        user_id=user_id,
        organization=org
    ).delete()

    messages.success(request, "Member removed.")
    return redirect("org_dashboard", org_id=org.id)


@login_required
def pending_invites(request, org_id):
    org = get_object_or_404(Organization, id=org_id)

    # Permission check
    is_allowed = Membership.objects.filter(
        user=request.user,
        organization=org,
        role__in=["admin", "manager"]
    ).exists()

    if not is_allowed:
        messages.error(request, "You do not have permission to view invites.")
        return redirect("org_dashboard", org_id=org.id)

    invites = OrganizationInvite.objects.filter(
        organization=org,
        accepted=False
    ).order_by("-created_at")

    context = {
        "organization": org,
        "invites": invites,
    }

    return render(request, "organization/pending_invites.html", context)
