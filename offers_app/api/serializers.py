from rest_framework import serializers

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
    details = PackageDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ('id', 'title', 'image', 'description', 'details')
        read_only_fields = ('user',)

    def validate_details(self, value):
        print(self.context.get("request").method)
        if self.context.get("request").method == 'POST' and len(value) != 3:
            raise serializers.ValidationError("An offer must contain exactly 3 details.")
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

        # Update Offer-Felder
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
