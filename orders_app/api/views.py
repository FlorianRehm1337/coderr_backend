from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Order
from .serializers import OrderSerializer
from ..helpers import get_user_profile, is_customer, is_business
from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import TokenAuthentication


class OrderModelViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filtert Orders basierend auf dem aktuellen User
        """
        user = self.request.user
        user_profile = get_user_profile(user)

        if not user_profile:
            return Order.objects.none()

        if is_customer(user):
            return Order.objects.filter(customer_user=user_profile)

        elif is_business(user):
            return Order.objects.filter(business_user=user_profile)

        if user.is_superuser or user.is_staff:
            return Order.objects.all()

        return Order.objects.none()

    def create(self, request, *args, **kwargs):
        """
        Erstellt eine neue Order
        """
        if not is_customer(request.user):
            return Response(
                {'error': 'Benutzer hat keine Berechtigung, z.B. weil nicht vom typ customer.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Wird automatisch beim Erstellen aufgerufen
        """
        serializer.save()

class OrderCountView(RetrieveAPIView):
    pass

class CompletedOrderCountView(RetrieveAPIView):
    pass
