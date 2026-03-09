from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# -------------------------------------------------------
# Custom User Model
# -------------------------------------------------------

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.username



# -------------------------------------------------------
# Organization Model
# -------------------------------------------------------

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_organizations",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name



# -------------------------------------------------------
# Membership Model (User ↔ Organization)
# -------------------------------------------------------

class Membership(models.Model):

    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self):
        return f"{self.user.username} → {self.organization.name} ({self.role})"
