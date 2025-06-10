from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User

from auth_app.api.serializers import BusinessProfileSerializer, CustomerProfileSerializer
from auth_app.models import BusinessProfile, CustomerProfile
from profile_app.api.serializers import ProfileSerializer
from profile_app.utils import build_data

class ProfileView(generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(user, 'customer'):
            user_role = user.customer
        elif hasattr(user, 'business'):
            user_role = user.business

        data = build_data(user, user_role)
        return Response(data, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        user = User.objects.get(id=pk)
        if user != request.user:
            return Response({"error": "Authentifizierter Benutzer ist nicht der Eigentümer Profils"}, status=status.HTTP_403_FORBIDDEN)
        if hasattr(request.user, 'customer'):
            serializer = CustomerProfileSerializer(request.user.customer, data=request.data, partial=True)
        if hasattr(request.user, 'business'):
            serializer = BusinessProfileSerializer(request.user.business, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessProfileListView(generics.RetrieveAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BusinessProfileSerializer

    def get(self, request):
        business_profiles = BusinessProfile.objects.all()
        serializer = BusinessProfileSerializer(business_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerProfileListView(generics.RetrieveAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer

    def get(self, request):
        customer_profiles = CustomerProfile.objects.all()
        serializer = CustomerProfileSerializer(customer_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
