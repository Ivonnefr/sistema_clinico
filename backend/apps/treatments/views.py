from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsActiveUser, IsDentist
from .models import CatalogProcedure, ExecutedProcedure, Budget, BudgetDetail
from django.db.models import Count, Q, Prefetch
from rest_framework.decorators import action
from rest_framework.response import Response

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
    
    
    def perform_create(self, serializer):
        serializer.save(dentist=self.request.user)
        
        
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
            queryset = Budget.objects.all()
        else:
            queryset = Budget.objects.filter(dentist=user)

        queryset = queryset.annotate(
            total_count=Count('details', distinct=True),
            executed_count=Count(
                'details',
                filter=Q(details__executions__isnull=False),
                distinct=True
            )
        ).prefetch_related(
            Prefetch(
                'details',
                queryset=BudgetDetail.objects.annotate(
                    executions_count=Count('executions')
                )
            )
        )

        return queryset
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == 'closed':
            raise PermissionDenied("No se puede editar un presupuesto cerrado")

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status == 'closed':
            raise PermissionDenied("No se puede eliminar un presupuesto cerrado")

        return super().destroy(request, *args, **kwargs)
    
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        original = self.get_object()

        # crear nuevo budget
        new_budget = Budget.objects.create(
            clinical_record=original.clinical_record,
            dentist=original.dentist,
            parent=original
        )

        # duplicar detalles
        for detail in original.details.all():
            BudgetDetail.objects.create(
                budget=new_budget,
                catalog_procedure=detail.catalog_procedure,
                piece=detail.piece,
                tooth_side=detail.tooth_side,
                scope=detail.scope,
                status=detail.status,
                price=detail.price
            )

        return Response({
            "message": "Presupuesto duplicado",
            "new_budget_id": new_budget.id
        })
            
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