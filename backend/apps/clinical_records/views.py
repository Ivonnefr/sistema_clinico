from django.shortcuts import render
from rest_framework import viewsets
from .models import ClinicalRecord
from .serializers import ClinicalRecordSerializer
from rest_framework.permissions import IsAuthenticated


class ClinicalRecordViewSet(viewsets.ModelViewSet):
    queryset = ClinicalRecord.objects.all()
    serializer_class = ClinicalRecordSerializer
    permission_classes = [IsAuthenticated]