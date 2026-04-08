from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import CatalogProcedure, ExecutedProcedure, Budget, BudgetDetail

from .serializers import (
    CatalogProcedureSerializer,
    ExecutedProcedureSerializer,
    BudgetSerializer,
    BudgetDetailSerializer
)

class CatalogProcedureViewSet(viewsets.ModelViewSet):
    queryset = CatalogProcedure.objects.all()
    serializer_class = CatalogProcedureSerializer
    permission_classes = [IsAuthenticated]
    
class ExecutedProcedureViewSet(viewsets.ModelViewSet):
    queryset = ExecutedProcedure.objects.all()
    serializer_class = ExecutedProcedureSerializer
    permission_classes = [IsAuthenticated]

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(dentist=self.request.user)
        
class BudgetDetailViewSet(viewsets.ModelViewSet):
    queryset = BudgetDetail.objects.all()
    serializer_class = BudgetDetailSerializer
    permission_classes = [IsAuthenticated]