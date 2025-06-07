from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):

    """
    Serializer for user profile.
    """
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    type = serializers.CharField(max_length=50, required=True)
    file = serializers.FileField(required=False, allow_null=True)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)
    tel = serializers.CharField(max_length=15, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    working_hours = serializers.CharField(max_length=100, required=False, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
