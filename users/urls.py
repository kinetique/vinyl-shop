from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from users.views import RegisterView, LoginView, UserProfileView, LogoutView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', UserProfileView.as_view(), name='user-profile'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
