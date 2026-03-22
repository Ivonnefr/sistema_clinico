from django.shortcuts import render
from rest_framework import viewsets
from .models import Atencion
from .serializers import AttentionSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsActiveUser, IsOdontologo

class AttentionViewSet(viewsets.ModelViewSet):
    queryset = Atencion.objects.all()
    serializer_class = AttentionSerializer

    def get_permissions(self):

        if self.action in ["list", "retrieve"]:
            permission_classes = [IsActiveUser, IsOdontologo]

        elif self.action == "create":
            permission_classes = [IsActiveUser, IsOdontologo]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsActiveUser, IsOdontologo]

        else:
            permission_classes = [IsActiveUser]

        return [permission() for permission in permission_classes]
