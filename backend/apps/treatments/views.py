from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsActiveUser, IsDentist
from .models import CatalogProcedure, ExecutedProcedure, Budget, BudgetDetail

from .serializers import (
    CatalogProcedureSerializer,
    ExecutedProcedureSerializer,
    BudgetSerializer,
    BudgetDetailSerializer
)
# query_set() que datos ve
# perform_create() qué datos crea
class CatalogProcedureViewSet(viewsets.ModelViewSet):
    queryset = CatalogProcedure.objects.all()
    serializer_class = CatalogProcedureSerializer

    def get_permissions(self):
        user = self.request.user

        if user.is_staff:
            permission_classes = [IsActiveUser]

        else:
            if self.action in ['list', 'retrieve']:
                permission_classes = [IsActiveUser]
            else:
                permission_classes = [IsActiveUser, IsDentist]

        return [permission() for permission in permission_classes]
    
    
class ExecutedProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = ExecutedProcedureSerializer
    queryset = ExecutedProcedure.objects.all()
    
    def get_permissions(self):
        user = self.request.user

        if user.is_staff:
            permission_classes = [IsActiveUser]

        else:
            if self.action in ['list', 'retrieve']:
                permission_classes = [IsActiveUser]
            else:
                permission_classes = [IsActiveUser, IsDentist]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return ExecutedProcedure.objects.all()
        
        return ExecutedProcedure.objects.filter(attention__dentist=user)


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    
    def get_permissions(self):
        user = self.request.user

        if user.is_staff:
            permission_classes = [IsActiveUser]

        else:
            if self.action in ['list', 'retrieve']:
                permission_classes = [IsActiveUser]
            else:
                permission_classes = [IsActiveUser, IsDentist]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Budget.objects.all()
        
        return Budget.objects.filter(dentist=user)

    def perform_create(self, serializer):
        serializer.save(dentist=self.request.user)
        
class BudgetDetailViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetDetailSerializer
    queryset = BudgetDetail.objects.all()
    
    def get_permissions(self):
        user = self.request.user

        if user.is_staff:
            permission_classes = [IsActiveUser]

        else:
            if self.action in ['list', 'retrieve']:
                permission_classes = [IsActiveUser]
            else:
                permission_classes = [IsActiveUser, IsDentist]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return BudgetDetail.objects.all()
        return BudgetDetail.objects.filter(budget__dentist=user)