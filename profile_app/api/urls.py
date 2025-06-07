from django.urls import path

from profile_app.api.views import BusinessProfileListView, CustomerProfileListView, ProfileView

urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile_detail'),
    path('profile/business/', BusinessProfileListView.as_view(), name='business_profile_list'),
    path('profile/customer/', CustomerProfileListView.as_view(), name='customer_profile_list'),
]
