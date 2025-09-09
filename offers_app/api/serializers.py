from rest_framework import serializers

from offers_app.filters import OfferFilterHelper
from offers_app.models import Feature, Offer, PackageDetail

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'name')

class PackageDetailSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)

    class Meta:
        model = PackageDetail
        exclude = ('offer',)

    def to_internal_value(self, data):
        features_list = data.get('features', [])

        if features_list and isinstance(features_list[0], str):
            features_list = [{'name': f} for f in features_list]
            data = data.copy()
            data['features'] = features_list

        return super().to_internal_value(data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['features'] = list(instance.features.values_list('name', flat=True))

        rep['price'] = float(instance.price)
        return rep


class OfferSerializer(serializers.ModelSerializer):
    # 👇 Immer noch für WRITE
    details = PackageDetailSerializer(many=True, write_only=True)

    # 👇 Dynamisch gefiltert für READ - nur ID und URL
    details = serializers.SerializerMethodField(read_only=True)

    # 👇 Neue Felder für min_price und min_delivery_time
    min_price = serializers.SerializerMethodField(read_only=True)
    min_delivery_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time')
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_details(self, obj):
        """
        Gib nur ID und URL für Details zurück
        """
        # Verwende vorgefilterte Details falls vorhanden
        if hasattr(obj, '_filtered_details'):
            details_list = obj._filtered_details
        else:
            # Fallback - verwende FilterHelper
            request = self.context.get('request')
            details_qs = obj.details.all()
            details_list = OfferFilterHelper.filter_details_by_request(details_qs, request)

        # Erstelle die Detail-Objekte mit ID und URL
        request = self.context.get('request')
        result = []
        for detail in details_list:
            detail_data = {
                'id': detail.id,
                'url': request.build_absolute_uri(f'/api/offerdetails/{detail.id}/') if request else f'/api/offerdetails/{detail.id}/'
            }
            result.append(detail_data)

        return result

    def get_min_price(self, obj):
        """
        Ermittele den minimalen Preis aus den gefilterten Details
        """
        if hasattr(obj, '_filtered_details'):
            details_list = obj._filtered_details
        else:
            request = self.context.get('request')
            details_qs = obj.details.all()
            details_list = OfferFilterHelper.filter_details_by_request(details_qs, request)

        if details_list:
            return min(detail.price for detail in details_list)
        return None

    def get_min_delivery_time(self, obj):
        """
        Ermittele die minimale Lieferzeit aus den gefilterten Details
        """
        if hasattr(obj, '_filtered_details'):
            details_list = obj._filtered_details
        else:
            request = self.context.get('request')
            details_qs = obj.details.all()
            details_list = OfferFilterHelper.filter_details_by_request(details_qs, request)

        if details_list:
            return min(detail.delivery_time_in_days for detail in details_list)
        return None

    def validate_details(self, value):
        request = self.context.get("request")
        if request and request.method in ['POST', 'PUT', 'PATCH']:
            for detail in value:
                if 'offer_type' not in detail:
                    raise serializers.ValidationError(
                        {"details": "Each detail must include 'offer_type'."}
                    )

            if request and request.method == 'POST' and len(value) != 3:
                raise serializers.ValidationError(
                    "An offer must contain exactly 3 details."
                )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features_data = detail_data.pop('features')
            detail = PackageDetail.objects.create(offer=offer, **detail_data)

            for feature_data in features_data:
                feature, _ = Feature.objects.get_or_create(name=feature_data['name'])
                detail.features.add(feature)

        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            for detail_data in details_data:
                offer_type = detail_data.get('offer_type')
                features_data = detail_data.pop('features', [])

                try:
                    detail = instance.details.get(offer_type=offer_type)
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
                    detail.features.clear()
                except PackageDetail.DoesNotExist:
                    detail = PackageDetail.objects.create(offer=instance, **detail_data)

                for feature_data in features_data:
                    feature, _ = Feature.objects.get_or_create(name=feature_data['name'])
                    detail.features.add(feature)

        return instance


class FilteredPackageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageDetail
        exclude = ('offer',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['features'] = list(instance.features.values_list('name', flat=True))
        rep['price'] = float(instance.price)
        return rep
