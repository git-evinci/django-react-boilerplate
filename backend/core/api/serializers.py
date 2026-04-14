"""Serializers for the API module.

This module provides serializers for converting Django models to/from JSON,
including the UserSerializer for the User model.
"""
from typing import ClassVar

from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        """Metadata for UserSerializer."""

        model = User
        fields: ClassVar = ["id", "username", "email", "is_staff"]