from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from apps.users.permissions import IsActiveUser, IsRecepcionista, IsOdontologo


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_permissions(self):

        # Ver citas
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsActiveUser]

        # Crear cita (solo recepcionista)
        elif self.action == "create":
            permission_classes = [IsActiveUser]

        # Actualizar
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsActiveUser]

        # Eliminar
        elif self.action == "destroy":
            permission_classes = [IsActiveUser, IsRecepcionista]

        else:
            permission_classes = [IsActiveUser]

        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer): # perform_create es un metodo que ya existe en Django REST Framework, se sobreescribe para agregar la logica de asignar el dentista automaticamente
        # Es un override
        user = self.request.user

        # Si es dentista, se asigna solo
        if hasattr(user, "odontologo"):
            serializer.save(dentist=user)

        # Si es recepcionista, usa el que viene del request
        else:
            serializer.save()