from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserSerializer
from The_Builder.models import Users

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer
import logging

logger = logging.getLogger(__name__)

class LoginView(APIView):
    """
    Manual login:
    - expects JSON: { "user_email": "...", "user_password": "..." }
    - returns JSON always (no HTML)
    """
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({"status": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.validated_data["user_email"]
            password = serializer.validated_data["user_password"]

            try:
                user = Users.objects.get(user_email=email)
            except Users.DoesNotExist:
                return Response({"status": False, "message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

            # check password
            if not check_password(password, user.user_password):
                return Response({"status": False, "message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

            # inactive user
            if not user.user_is_active:
                return Response({"status": False, "message": "Account disabled"}, status=status.HTTP_403_FORBIDDEN)

            # create tokens inside try to catch any token-related errors
            try:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
            except Exception as e:
                logger.exception("Failed to create JWT tokens for user %s", user.user_email)
                return Response({"status": False, "message": "Could not create auth tokens"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # success
            return Response({
                "status": True,
                "message": "Login successful",
                "data": {
                    "user_id": user.user_id,
                    "full_name": user.user_full_name,
                    "email": user.user_email,
                    "username": user.user_username,
                    "phone": user.user_phone,
                    "user_type": user.user_type,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            }, status=status.HTTP_200_OK)

        except Exception as exc:
            # This will ensure Django debug HTML is not returned to client.
            logger.exception("Unhandled error in LoginView: %s", exc)
            return Response({"status": False, "message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
