from rest_framework import serializers
from .models import User
#El serializer convierte el modelo User en un formato JSON para que pueda ser enviado a través de la API
#El serializer para el endpoint /me/ que devuelve la información del usuario autenticado
#cuando pida el /me le va a devolver el id y el email del usuario autenticado

class MeSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "email", "role"]
    def get_role(self, obj):
        if hasattr(obj, 'odontologo'):
            return 'odontologo'
        if hasattr(obj, 'recepcionista'):
            return 'recepcionista'
        else:
            return 'admin'