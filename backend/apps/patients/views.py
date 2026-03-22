from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from users.permissions import IsOdontologo, IsRecepcionista, IsStaff

# PatientViewSet es una vista que maneja las operaciones CRUD para el modelo Patient, se va a usar para el endpoint /patients/ y se le asigna el permiso IsAuthenticated para que solo los usuarios autenticados puedan acceder a esta vista, si no estás autenticado te va a devolver un error 401 Unauthorized
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
    def get_permissions(self):

        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated, IsStaff]

        elif self.action == "create":
            permission_classes = [IsAuthenticated, IsRecepcionista]

        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOdontologo]

        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOdontologo]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]