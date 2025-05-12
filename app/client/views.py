"""
View modules for the Client API.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Client
from client import serializers


class ClientViewSet(viewsets.ModelViewSet):
    """
    View for managing client APIs.
    """

    serializer_class = serializers.ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the clients for the authenticated user.
        """
        return self.queryset.filter(user=self.request.user).order_by("-id")
