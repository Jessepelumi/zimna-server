import os
import hmac
import secrets
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer, RegisterSerializer
from .throttles import LoginThrottle, OTPSendThrottle, OTPVerifyThrottle

User = get_user_model()

OTP_TTL_SECONDS = 300
OTP_MAX_ATTEMPTS = 5
OTP_LOCKOUT_SECONDS = 300

def _issue_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": UserSerializer(user).data
    }


# FLOW 1: EMAIL & PASSWORD (Credentials)

class RegisterView(APIView):
    """Creates a new user account with Email & Password."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(_issue_tokens(user), status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordLoginView(APIView):
    """Authenticates existing users via Email & Password."""
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginThrottle]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        email = email.lower().strip()
        
        # Authenticates against Django's PBKDF2 password hasher
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "Account is disabled."}, status=status.HTTP_403_FORBIDDEN)

        return Response(_issue_tokens(user), status=status.HTTP_200_OK)


# FLOW 2: EMAIL & OTP (Passwordless)

class SendOTPView(APIView):
    """Generates a 6-digit verification code and emails it to the user."""
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPSendThrottle]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

        email = email.lower().strip()

        # Cryptographically secure 6-digit string
        otp_code = f"{secrets.randbelow(1000000):06d}"

        # Save to Redis/Cache with a 5-minute (300s) TTL
        cache.set(f"otp:{email}", otp_code, timeout=OTP_TTL_SECONDS)

        # Reset any prior wrong-attempt count whenever a fresh code is issued
        cache.delete(f"otp_attempts:{email}")

        # Dispatch email
        send_mail(
            subject="Your Yiyara Login Code",
            message=f"Your verification code is: {otp_code}. It expires in 5 minutes.",
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "Verification code sent."}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    """Validates the 6-digit OTP code and logs the user in (creating account if new)."""
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OTPVerifyThrottle]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"error": "Email and code required"}, status=status.HTTP_400_BAD_REQUEST)

        email = email.lower().strip()
        attempts_key = f"otp_attempts:{email}"
        lockout_key = f"otp_lockout:{email}"

        # Hard lockout: too many wrong guesses against the current code
        if cache.get(lockout_key):
            return Response(
                {"error": "Too many incorrect attempts. Request a new code and try again shortly."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        cache_key = f"otp:{email}"
        cached_otp = cache.get(cache_key)

        if not cached_otp or not hmac.compare_digest(str(cached_otp), str(code)):
            # Count the failed attempt and lock out once the limit is hit
            attempts = cache.get(attempts_key, 0) + 1
            cache.set(attempts_key, attempts, timeout=OTP_TTL_SECONDS)

            if attempts >= OTP_MAX_ATTEMPTS:
                cache.get(lockout_key, True, timeout=OTP_LOCKOUT_SECONDS)
                cache.delete(cache_key)

                return Response(
                    {"error": "Too many incorrect attempts. Request a new code and try again shortly."}, 
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )

            return Response({"error": "Invalid or expired code."}, status=status.HTTP_400_BAD_REQUEST)

        # Success — clear code and attempt counter to prevent replay attacks
        cache.delete(cache_key)
        cache.delete(attempts_key)

        # Fetch or create user (Uses custom UserManager)
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'is_email_verified': True}
        )

        if not created and not user.is_email_verified:
            user.is_email_verified = True
            user.save(update_fields=['is_email_verified'])

        return Response(_issue_tokens(user), status=status.HTTP_200_OK)


# FLOW 3: OAUTH (NextAuth Server-to-Server)

class InternalAuthView(APIView):
    """Exchanges NextAuth provider data for Django JWTs via secured internal secret."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        server_secret = os.getenv("INTERNAL_AUTH_SECRET")
        client_secret = request.headers.get("X-Internal-Secret")

        if not server_secret or not client_secret or not hmac.compare_digest(client_secret, server_secret):
            return Response({"error": "Unauthorized internal request"}, status=status.HTTP_401_UNAUTHORIZED)

        email = request.data.get("email")
        if not email:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

        email = email.lower().strip()

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': request.data.get("first_name", ""),
                'last_name': request.data.get("last_name", ""),
                'is_email_verified': True,
            }
        )

        if not created and not user.is_email_verified:
            user.is_email_verified = True
            user.save(update_fields=['is_email_verified'])

        return Response(_issue_tokens(user), status=status.HTTP_200_OK)
    