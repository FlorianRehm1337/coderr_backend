from django.urls import path
from .views import CompletedOrderCountView, OrderCountView, OrderModelViewset
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'orders', OrderModelViewset)

urlpatterns = [
    *router.urls,
    path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
    ]
