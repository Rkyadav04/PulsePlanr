
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from core.profile_forms import ProfileUpdateForm
from core.models import Membership, Organization
from core.invite_models import OrganizationInvite
from django.utils import timezone

def register_view(request):
    invite_token = request.GET.get("invite")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect to invite acceptance if token exists
            if invite_token:
                return redirect("accept_invite", token=invite_token)

            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    invite_token = request.POST.get("invite") or request.GET.get("invite")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())

            if invite_token:
                return redirect("accept_invite", token=invite_token)

            return redirect("dashboard")
    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})




def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def profile_view(request):
    user = request.user

    # List organizations the user belongs to
    orgs = Membership.objects.filter(user=user).select_related("organization")

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'profile/profile.html', {
        'form': form,
        'user': user,
        'orgs': orgs,
    })

@login_required
def dashboard_view(request):
    user = request.user
    now = timezone.now()

    # 1️⃣ Organizations owned by the user
    owned_orgs = Organization.objects.filter(owner=user)

    # 2️⃣ Organizations user is a member of
    memberships = ( 
        Membership.objects
        .select_related("organization")
        .filter(user=request.user)
    )

    # 3️⃣ Invites sent by the user (still pending)
    sent_invites = OrganizationInvite.objects.filter(
        invited_by=user,
        accepted=False
    ).select_related("organization")

    # 4️⃣ Invites received by the user (still valid)
    received_invites = OrganizationInvite.objects.filter(
        email=user.email,
        accepted=False
    ).filter(
        expires_at__isnull=True
    ) | OrganizationInvite.objects.filter(
        email=user.email,
        accepted=False,
        expires_at__gt=now
    )

    context = {
        "owned_orgs": owned_orgs,
        "memberships": memberships,
        "sent_invites": sent_invites,
        "received_invites": received_invites,
 
        
    }

    return render(request, "dashboard.html", context)

def register_view(request):
    invite_token = request.GET.get("invite")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Redirect to invite acceptance if token exists
            if invite_token:
                return redirect("accept_invite", token=invite_token)

            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})
