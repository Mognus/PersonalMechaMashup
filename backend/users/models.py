from django.db import models

# Create your models here.
      
# backend/users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _ # For translating help texts etc.

class CustomUser(AbstractUser):
    """
    Custom user model inheriting from AbstractUser.
    Provides standard fields like username, email, password, first_name, last_name, etc.
    You can add custom fields here later.
    """

    # Example of adding a new field (currently commented out):
    # bio = models.TextField(_('Biography'), blank=True, null=True)
    # profile_picture = models.ImageField(_('Profile Picture'), upload_to='profile_pics/', blank=True, null=True)

    # --- Override related_name for groups and user_permissions ---
    # This is necessary to avoid clashes with the default auth.User model's
    # related names if you ever have both User models active or use certain third-party apps.
    # It's good practice even when replacing the default user model entirely.

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customuser_groups", # Changed related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_permissions", # Changed related_name
        related_query_name="user",
    )

    def __str__(self):
        """String representation of the user."""
        return self.username

    # You can add custom methods to your user model here
    # def get_full_display_name(self):
    #     return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        # Optional: Define ordering, e.g., by username
        # ordering = ['username']

    