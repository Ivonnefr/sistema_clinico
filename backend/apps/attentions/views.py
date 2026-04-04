from django.shortcuts import render
from rest_framework import viewsets
from .models import Attention
from .serializers import AttentionSerializer
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsActiveUser, IsDentist

class AttentionViewSet(viewsets.ModelViewSet):
    queryset = Attention.objects.all()
    serializer_class = AttentionSerializer

    def get_permissions(self):

        if self.action in ["list", "retrieve"]:
            permission_classes = [IsActiveUser, IsDentist]

        elif self.action == "create":
            permission_classes = [IsActiveUser, IsDentist]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsActiveUser, IsDentist]

        else:
            permission_classes = [IsActiveUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        patient = serializer.validated_data['patient'] # Obtener el objeto Patient

        serializer.save(
            dentist=self.request.user, # El usuario autenticado o sea el dentista que hace la consulta
            clinical_record=patient.clinical_record # Obtener la ficha clinica del paciente
        )
        
    def get_queryset(self):
        user = self.request.user

        # Admin ve todo
        if user.is_staff:
            return Attention.objects.all()

        # Dentista ve solo sus atenciones
        return Attention.objects.filter(dentist=user)
    
