from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CatalogProcedureViewSet, ExecutedProcedureViewSet, BudgetViewSet, BudgetDetailViewSet

router = DefaultRouter()
router.register(r'catalog-procedures', CatalogProcedureViewSet)
router.register(r'executed-procedures', ExecutedProcedureViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'budget-details', BudgetDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]