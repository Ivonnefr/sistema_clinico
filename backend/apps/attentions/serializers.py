from rest_framework import serializers
from .models import Atencion

class AttentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atencion
        fields = '__all__'