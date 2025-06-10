from django.http import Http404
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from offers_app.api.permissions import IsBusinessAccount, IsOfferCreator
from offers_app.api.serializers import OfferSerializer
from offers_app.models import Offer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound


class OfferModelViewset(ModelViewSet):

    serializer_class = OfferSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    queryset = Offer.objects.all()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound(detail="Offer not found.")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        self.instance = Offer.objects.get(pk=serializer.instance.pk)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsBusinessAccount]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsBusinessAccount, IsOfferCreator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
