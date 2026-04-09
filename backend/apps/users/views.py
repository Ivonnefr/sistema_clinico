from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MeSerializer

class MeView(APIView): #MeView es una vista que devuelve la información del usuario autenticado, se va a usar para el endpoint /me/
    permission_classes = [IsAuthenticated] # Solo los usuarios autenticados pueden acceder a esta vista, si no estás autenticado te va a devolver un error 401 Unauthorized

    def get(self, request):
        serializer = MeSerializer(request.user) # request.user es el usuario autenticado que hizo la petición, viene del jwt
        return Response(serializer.data) # Response es una clase de rest_framework que devuelve una respuesta HTTP con el contenido que le pasamos, en este caso el serializer.data que es la información del usuario autenticado en formato JSON