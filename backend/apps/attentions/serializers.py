from rest_framework import serializers
from .models import Attention
class AttentionSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True)
    dentist = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Attention
        fields = '__all__'
    
    def validate(self, data):
        if data['appointment'].patient != data['patient']:
            raise serializers.ValidationError(
                "Appointment does not belong to this patient"
            )
        return data