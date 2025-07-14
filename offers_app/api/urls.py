from django.urls import path
from .views import OfferDetailsView, OfferModelViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'offers', OfferModelViewset)

urlpatterns = [
    *router.urls,
    path('offerdetails/<int:pk>/', OfferDetailsView.as_view(), name='offer-details'),
    ]
