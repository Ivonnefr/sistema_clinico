from rest_framework.routers import DefaultRouter
from .views import AttentionViewSet

router = DefaultRouter()
router.register(r'attentions', AttentionViewSet)

urlpatterns = router.urls
