from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()

# Option 1: Keep ReadOnlyModelViewSet but restrict list/retrieve to Admins
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed.
    - Admins can list all users and retrieve any user.
    - Authenticated users can access their own profile via the 'me' action.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - 'me' action requires only authentication.
        - Other actions ('list', 'retrieve') require admin privileges.
        """
        if self.action == 'me':
            # Any authenticated user can access their own profile
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            # Only admin users can list all users or retrieve specific users by ID
            self.permission_classes = [permissions.IsAdminUser]
        else:
            # Default deny all for safety, though ReadOnlyViewSet shouldn't have other actions
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        """
        Retrieve, update or partial update the profile of the currently authenticated user.
        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(user, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Option 2: More explicit approach using APIView for '/me/' and restricting the ViewSet entirely (Alternative)
# You could remove the UserViewSet entirely if you ONLY want the '/me/' endpoint
# and potentially have an admin-only ViewSet elsewhere. Or structure it like this:

# class CurrentUserView(generics.RetrieveUpdateAPIView):
#     """
#     Handles GET, PUT, PATCH requests for the current authenticated user's profile.
#     Accessible via /api/me/ (needs URL adjustment in urls.py)
#     """
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_object(self):
#         # Returns the user associated with the request token
#         return self.request.user

# And keep a ViewSet ONLY for Admins:
# class AdminUserViewSet(viewsets.ModelViewSet): # Full CRUD for admins
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAdminUser] # Only admins allowed

# Then in urls.py you would register AdminUserViewSet and add a path for CurrentUserView.