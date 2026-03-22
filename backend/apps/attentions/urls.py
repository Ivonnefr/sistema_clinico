from rest_framework.routers import DefaultRouter
from .views import AtencionViewSet

router = DefaultRouter()
router.register(r'attentions', AtencionViewSet)

urlpatterns = router.urls