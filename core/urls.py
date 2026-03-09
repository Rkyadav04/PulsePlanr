from django.urls import path
from .views import (
    register_view, login_view, logout_view,
    dashboard_view
)

from .org_views import ( create_organization, org_dashboard, invite_member, accept_invite, remove_member, pending_invites)
from .admin_views import org_settings, update_org, change_role, delete_org
from .views import profile_view
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('organization/create/', create_organization, name='create_organization'),
    path('organization/<int:org_id>/', org_dashboard, name='org_dashboard'),
    path('organization/<int:org_id>/invite/', invite_member, name='invite_member'),
    path("organization/accept/<str:token>/", accept_invite, name="accept_invite"),
    path('organization/<int:org_id>/remove/<int:user_id>/', remove_member, name='remove_member'),
    path("organization/<int:org_id>/invites/",pending_invites, name="pending_invites"),

]


urlpatterns += [
    path('organization/<int:org_id>/settings/', org_settings, name='org_settings'),
    path('organization/<int:org_id>/settings/update/', update_org, name='update_org'),
    path('organization/<int:org_id>/settings/role/<int:user_id>/', change_role, name='change_role'),
    path('organization/<int:org_id>/settings/delete/', delete_org, name='delete_org'),
]



urlpatterns += [
    path('profile/', profile_view, name='profile'),
]
