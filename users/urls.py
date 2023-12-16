from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name = 'register'),
    # Profile page
    path('profile/new', views.UserProfileCreateView.as_view(), name='profile-creation'),
    path('profile/<pk>', views.UserProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<pk>/update', views.UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<pk>/delete', views.UserProfileDeleteView.as_view(), name='profile-delete'),

]
