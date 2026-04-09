from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClinicalRecordViewSet, ClinicalEvolutionViewSet

router = DefaultRouter()
router.register(r'clinical-records', ClinicalRecordViewSet)
router.register(r'evolutions', ClinicalEvolutionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]