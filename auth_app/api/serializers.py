from rest_framework import serializers

from auth_app.models import BusinessProfile, CustomerProfile

class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        """
        Validate that password and repeated_password match.
        """
        password = data.get('password')
        repeated_password = data.get('repeated_password')
        if password != repeated_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class CustomerProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    file = serializers.FileField(required=False)
    uploaded_at = serializers.DateTimeField(required=False)
    type = serializers.CharField(max_length=50, default='customer')

    class Meta:

        model = CustomerProfile
        exclude = ('id')

class BusinessProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    file = serializers.FileField(required=False)
    location = serializers.CharField(max_length=255, required=False)
    tel = serializers.CharField(max_length=15, required=False)
    description = serializers.CharField(required=False)
    working_hours = serializers.CharField(max_length=100, required=False)
    type = serializers.CharField(max_length=50, default='business')

    class Meta:

        model = BusinessProfile
        exclude = ('id')
