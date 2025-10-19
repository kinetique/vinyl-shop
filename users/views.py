from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        logger.info(f"Registration attempt: {request.data.get('email')}")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User registered successfully: {user.username} ({user.id})")
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email},
                status=status.HTTP_201_CREATED)
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        logger.info(f"Login attempt: {email}")
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f"Login failed: user with email {email} does not exist")
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=user.username, password=password)
        if user is None:
            logger.warning(f"Login failed: incorrect password for {email}")
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        logger.info(f"User logged in successfully: {email}")
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logger.info(f"Profile fetched for user: {user.username} ({user.id})")
        return Response({"username": user.username, "email": user.email})

    def put(self, request):
        user = request.user
        username = request.data.get('username', user.username)
        email = request.data.get('email', user.email)
        logger.info(f"Profile update attempt for user {user.username} ({user.id})")

        if not username:
            logger.warning("Profile update failed: username empty")
            return Response({"error": "Username cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            logger.warning("Profile update failed: email empty")
            return Response({"error": "Email cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        user.username = username
        user.email = email
        user.save()
        logger.info(f"Profile updated successfully for user {user.username} ({user.id})")
        Response({"username": user.username, "email": user.email}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Logout attempt by user: {request.user.username} ({request.user.id})")
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.username} logged out successfully")
            return Response({"detail": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Logout failed for user {request.user.username}: {str(e)}")
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
