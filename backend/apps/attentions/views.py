from django.shortcuts import render
from rest_framework import viewsets
from .models import Attention
from .serializers import AttentionSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsActiveUser, IsOdontologo

class AttentionViewSet(viewsets.ModelViewSet):
    queryset = Attention.objects.all()
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

    def perform_create(self, serializer):
        serializer.save(dentist=self.request.user)
        
    def get_queryset(self):
        user = self.request.user

        # Admin ve todo
        if user.is_staff:
            return Attention.objects.all()

        # Dentista ve solo sus atenciones
        return Attention.objects.filter(dentist=user)