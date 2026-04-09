from rest_framework import serializers
from .models import ClinicalRecord, ClinicalEvolution

class ClinicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalRecord
        fields = '__all__'
        read_only_fields = ['patient', 'opened_at']
        
class ClinicalEvolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalEvolution
        fields = '__all__'
        read_only_fields = ['created_at']