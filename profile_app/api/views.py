from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User

from auth_app.api.serializers import BusinessProfileSerializer, CustomerProfileSerializer
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
        else:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        data = build_data(user, user_role)
        return Response(data)


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
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessProfileListView(generics.RetrieveAPIView):

    def get():
        pass


class CustomerProfileListView(generics.RetrieveAPIView):

    def get():
        pass
