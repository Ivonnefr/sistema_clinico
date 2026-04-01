from rest_framework import serializers
from .models import ClinicalRecord


class ClinicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalRecord
        fields = '__all__'
        read_only_fields = ['patient', 'opened_at']