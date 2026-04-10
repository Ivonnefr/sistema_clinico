from django.urls import path
from .views import FinancialDashboardAPIView

urlpatterns = [
    path('financial/', FinancialDashboardAPIView.as_view()),
]