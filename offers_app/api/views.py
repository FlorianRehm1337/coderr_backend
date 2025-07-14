from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from offers_app.api.permissions import IsBusinessAccount, IsOfferCreator
from offers_app.api.serializers import OfferSerializer, PackageDetailSerializer
from offers_app.models import Offer, PackageDetail
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
import django_filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='id')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name='delivery_time_in_days', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ['creator_id']

class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

class OfferModelViewset(ModelViewSet):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']
    pagination_class = OfferPagination

    def get_queryset(self):
        qs = super().get_queryset()
        min_price = self.request.query_params.get('min_price')
        max_delivery_time = self.request.query_params.get('max_delivery_time')

        if min_price:
            try:
                qs = qs.filter(details__price__gte=float(min_price))
            except ValueError:
                pass

        if max_delivery_time:
            try:
                qs = qs.filter(details__delivery_time_in_days__lte=int(max_delivery_time))
            except ValueError:
                pass

        return qs.distinct()

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
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsBusinessAccount]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsBusinessAccount, IsOfferCreator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class OfferDetailsView(RetrieveAPIView):
    queryset = PackageDetail.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PackageDetailSerializer
    def get_object(self):
        offer_detail_id = self.kwargs['pk']
        offer_detail = get_object_or_404(PackageDetail, id=offer_detail_id)
        return offer_detail
