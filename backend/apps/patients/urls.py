from rest_framework.routers import DefaultRouter
from .views import PatientViewSet

router = DefaultRouter() #crea un router para manejar las rutas de la API de pacientes
router.register(r'patients', PatientViewSet) #registra el viewset de pacientes en el router, el primer argumento es el prefijo de la ruta, en este caso /patients/ y el segundo argumento es el viewset que va a manejar las peticiones a esa ruta, en este caso PatientViewSet que es una vista que maneja las operaciones CRUD para los pacientes

urlpatterns = router.urls #urlpatterns es una lista de rutas que se va a usar en el archivo config/urls.py para incluir las rutas de la API de pacientes, router.urls es una propiedad del router que devuelve todas las rutas registradas en el router, en este caso solo tenemos una ruta /patients/ que maneja las operaciones CRUD para los pacientes   