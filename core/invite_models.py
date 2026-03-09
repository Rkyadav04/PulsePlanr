from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string
from core.models import Organization
from django.utils import timezone
from datetime import timedelta

class OrganizationInvite(models.Model):
    email = models.EmailField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default="employee")
    token = models.CharField(max_length=64, unique=True, blank=True)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    


    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(48)
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=3)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Invite {self.email} → {self.organization.name}"
