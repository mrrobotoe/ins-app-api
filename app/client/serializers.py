"""
Serializers for the Client API.
"""
from rest_framework import serializers

from core.models import Client


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model.
    """

    class Meta:
        model = Client
        fields = ["id", "name", "main_address", "phone_number", "email"]
        read_only_fields = ["id"]
