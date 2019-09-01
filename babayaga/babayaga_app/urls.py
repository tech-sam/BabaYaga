from rest_framework import routers
from .api import DbPropsViewSet

router = routers.DefaultRouter()
router.register('api/babayaga',DbPropsViewSet,'babayaga')

urlpatterns = router.urls