"""API views for user management."""
from rest_framework import viewsets

from ..models.user import User  # Adjust path based on your exact tree
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing User objects."""

    queryset = User.objects.all()
    serializer_class = UserSerializer