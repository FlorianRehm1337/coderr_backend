from django.urls import path
from .views import OfferModelViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'offers', OfferModelViewset)

urlpatterns = router.urls
