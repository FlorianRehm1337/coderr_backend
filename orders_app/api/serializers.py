# orders_app/api/serializers.py
from rest_framework import serializers

from offers_app.models import PackageDetail
from ..models import Order, Offer

class OrderSerializer(serializers.ModelSerializer):
    # Input field für offer_detail_id
    offer_detail_id = serializers.IntegerField(write_only=True)

    # Output fields (read-only)
    offer = serializers.SerializerMethodField(read_only=True)
    customer_user = serializers.SerializerMethodField(read_only=True)
    business_user = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    revisions = serializers.SerializerMethodField(read_only=True)
    delivery_time_in_days = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    features = serializers.SerializerMethodField(read_only=True)
    offer_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'offer_detail_id', 'customer_user', 'business_user',
            'offer', 'title', 'revisions', 'delivery_time_in_days',
            'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_offer(self, obj):
        return obj.offer.id if obj.offer else None

    def get_customer_user(self, obj):
        return obj.customer_user.id if obj.customer_user else None

    def get_business_user(self, obj):
        return obj.business_user.id if obj.business_user else None

    def get_title(self, obj):
        return obj.offer.title if obj.offer else None

    def get_revisions(self, obj):
        return obj.offer.revisions if obj.offer else None

    def get_delivery_time_in_days(self, obj):
        return obj.offer.delivery_time_in_days if obj.offer else None

    def get_price(self, obj):
        return obj.offer.price if obj.offer else None

    def get_features(self, obj):
        return obj.offer.features if obj.offer else None

    def get_offer_type(self, obj):
        return obj.offer.offer_type if obj.offer else None

    def validate_offer_detail_id(self, value):
        """
        Validiert, dass das Angebot existiert
        """
        try:
            offer_detail = PackageDetail.objects.get(id=value)
            return value
        except Offer.DoesNotExist:
            raise serializers.ValidationError("Das angegebene Angebotsdetail wurde nicht gefunden.")

    def create(self, validated_data):
        """
        Erstellt eine Order basierend auf offer_detail_id
        """
        offer_detail_id = validated_data.pop('offer_detail_id')

        try:
            offer_detail = PackageDetail.objects.get(id=offer_detail_id)
        except Offer.DoesNotExist:
            raise serializers.ValidationError("Das angegebene Angebotsdetail wurde nicht gefunden.")

        # User-Typ über type Property prüfen
        user = self.context['request'].user
        customer_profile = None

        # Prüfe Customer Profile
        if hasattr(user, 'customer') and user.customer.type == 'customer':
            customer_profile = user.customer

        if not customer_profile:
            raise serializers.ValidationError("Benutzer hat keine Berechtigung, z.B. weil nicht vom typ 'customer'.")

        order = Order.objects.create(
            customer_user=customer_profile,
            business_user=offer_detail.offer.user.business,
            offer_detail=offer_detail,
            status='in_progress'
        )

        return order
