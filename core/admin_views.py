from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Organization, Membership, User

# Ensure current user is admin of this org
def admin_required(view_func):
    def wrapper(request, org_id, *args, **kwargs):
        org = get_object_or_404(Organization, id=org_id)
        membership = Membership.objects.filter(user=request.user, organization=org).first()

        if not membership or membership.role != 'admin':
            return redirect("org_dashboard", org_id=org_id)

        return view_func(request, org_id, org, membership, *args, **kwargs)
    return wrapper


@login_required
@admin_required
def org_settings(request, org_id, org, membership):
    members = Membership.objects.filter(organization=org)
    return render(request, "organization/org_settings.html", {
        "org": org,
        "members": members,
    })


@login_required
@admin_required
def update_org(request, org_id, org, membership):
    if request.method == "POST":
        org.name = request.POST.get("name")
        org.description = request.POST.get("description")
        org.save()
        return redirect("org_settings", org_id=org.id)
    return redirect("org_settings", org_id=org.id)


@login_required
@admin_required
def change_role(request, org_id, org, membership, user_id):
    member = get_object_or_404(Membership, organization=org, user_id=user_id)

    if request.method == "POST":
        new_role = request.POST.get("role")

        # admin cannot demote themselves
        if member.user == request.user:
            return redirect("org_settings", org_id=org.id)

        member.role = new_role
        member.save()

    return redirect("org_settings", org_id=org.id)


@login_required
@admin_required
def delete_org(request, org_id, org, membership):
    if request.method == "POST":
        org.delete()
        return redirect("dashboard")
    return redirect("org_settings", org_id=org.id)
