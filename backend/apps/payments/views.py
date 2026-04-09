from django.shortcuts import render
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from apps.users.permissions import IsActiveUser, IsDentist, IsReceptionist
from rest_framework.permissions import IsAdminUser


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

def get_permissions(self):
    user = self.request.user

    if user.is_staff:
        permission_classes = [IsActiveUser]

    else:
        if self.action in ['list', 'retrieve']:
            # ver pagos
            permission_classes = [IsActiveUser]

        else:
            # crear / editar pagos
            permission_classes = [IsActiveUser, (IsDentist | IsReceptionist)]

    return [permission() for permission in permission_classes]