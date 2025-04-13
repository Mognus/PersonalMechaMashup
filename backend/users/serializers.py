from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.
    Specifies the fields to be included when serializing/deserializing User objects.
    """
    class Meta:
        model = CustomUser
        # Specify the fields to include in the API representation
        fields = [
            'id',           # User ID
            'username',     # Username
            'email',        # Email address
            'first_name',   # First name
            'last_name',    # Last name
            # Add any custom fields you added to CustomUser here later
            # 'bio',
            # 'profile_picture',
            'is_active',    # Is the user account active?
            'is_staff',     # Is the user a staff member (can access admin)?
            'date_joined',  # Date the user registered
            'last_login',   # Last login timestamp
        ]
        # Specify fields that should be read-only (cannot be set directly via API update/create)
        read_only_fields = [
            'id',
            'is_active',    # Usually managed by admin or activation logic
            'is_staff',     # Usually managed by admin
            'date_joined',
            'last_login',
        ]

        # Optional: Add extra constraints or validations if needed
        # extra_kwargs = {
        #     'password': {'write_only': True, 'min_length': 8}, # Example for password if included
        # }

    # Note: We deliberately exclude the 'password' field here for security.
    # Password handling (setting/changing) usually requires separate, dedicated endpoints/logic.
    # We also exclude 'groups' and 'user_permissions' for simplicity,
    # they could be added if needed (potentially with nested serializers).