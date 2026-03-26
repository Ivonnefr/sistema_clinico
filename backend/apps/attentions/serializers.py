from rest_framework import serializers
from .models import Attention
class AttentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attention
        fields = '__all__'
        read_only_fields = ['dentist']