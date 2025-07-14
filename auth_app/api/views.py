from rest_framework import generics
from rest_framework.response import Response
from auth_app.models import CustomerProfile, BusinessProfile
from django.contrib.auth.models import User

from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token


class RegistrationView(generics.CreateAPIView):

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    """
    View for user registration.
    """
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
            )
            if serializer.validated_data['type'] == 'customer':
                CustomerProfile.objects.create(user=new_user)
            else:
                BusinessProfile.objects.create(user=new_user)
            token = Token.objects.create(user=new_user)
            return Response({
                "token": token.key,
                "username": new_user.username,
                "email": new_user.email,
                "user_id": new_user.id,
            }, status=201)
        return Response(serializer.errors, status=400)


class LoginView(generics.ListAPIView):

    permission_classes = [AllowAny]
    def post(self, request):
        """
        View for user login.
        """
        user = User.objects.get(username=request.data['username'])
        correct_password = user.check_password(request.data['password'])
        user_token = Token.objects.get_or_create(user=user.id)
        if user and correct_password is True:
            return Response({
                "token": user_token[0].key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }, status=200)
        return Response({"detail": "Ungültige Anfragedaten gesendet."}, status=400)
