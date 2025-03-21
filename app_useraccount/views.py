from django.conf import settings
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, OTPVerifySerializer, LoginSerializer
from .models import User


''' Create your views here '''

# Generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refreshToken': str(refresh),
        'accessToken': str(refresh.access_token),
    }
        

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        email = request.data.get('email')

        # Check if user already exists
        user = User.objects.filter(email=email).first()

        if user:
            if not user.is_active:
                # Generate a new OTP
                user.otp = get_random_string(length=6, allowed_chars='0123456789')
                user.otp_created_at = timezone.now()
                user.save()

                # Send new OTP via email
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP code is {user.otp}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )

                # return Response(
                #     {'error': 'User exists but is inactive. A new OTP has been sent to your email.'},
                #     status=status.HTTP_403_FORBIDDEN
                # )

                return Response(
                    {'msg': 'An OTP is sent to your email.', 'email': email},
                    status=status.HTTP_403_FORBIDDEN
                )

            return Response({'error': 'User with this email already exists.'}, status=status.HTTP_409_CONFLICT)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'msg': 'An OTP is sent to your email.', 'email': serializer.data.get('email')}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            if 'email' in e.detail:
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_409_CONFLICT)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

    


class OTPVerifyView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = get_tokens_for_user(user)
            return Response({
                'msg': 'User verification successful',
                'token': token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Logged in successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token

            return Response({"msg": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RefreshBothTokensUnauthUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):        
        try:
            refresh_token = request.data.get("refresh_token")
            
            # Validate and parse the refresh token
            token = RefreshToken(refresh_token)

            user_id = token["user_id"]

            user = User.objects.get(id=user_id)

            # Blacklist the old refresh token
            token.blacklist()

            # Generate new tokens for the user
            new_tokens = get_tokens_for_user(user)
            
            return Response({
                'refreshToken': new_tokens['refreshToken'],
                'accessToken': new_tokens['accessToken'],
                'msg': 'Tokens refreshed successfully'
            }, status=status.HTTP_200_OK)
        
        except TokenError as e:
            return Response({"error": "Invalid token or token has been blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RefreshAccessTokenUnauthUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):        
        try:
            refresh_token = request.data.get("refresh_token")
            
            # Validate and parse the refresh token
            refresh = RefreshToken(refresh_token)
            
            return Response({
                'accessToken': str(refresh.access_token),
                'msg': 'Access token refreshed successfully'
            }, status=status.HTTP_200_OK)
        
        except TokenError as e:
            return Response({"error": "Invalid token or token has been blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class RefreshBothTokensAuthUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):        
        try:
            refresh_token = request.data.get("refresh_token")
            
            # Validate and parse the refresh token
            token = RefreshToken(refresh_token)

            user_id = token["user_id"]

            user = User.objects.get(id=user_id)

            # Blacklist the old refresh token
            token.blacklist()

            # Generate new tokens for the user
            new_tokens = get_tokens_for_user(user)
            
            return Response({
                'refreshToken': new_tokens['refreshToken'],
                'accessToken': new_tokens['accessToken'],
                'msg': 'Tokens refreshed successfully'
            }, status=status.HTTP_200_OK)
        
        except TokenError as e:
            return Response({"error": "Invalid token or token has been blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RefreshAccessTokenAuthUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):        
        try:
            refresh_token = request.data.get("refresh_token")
            
            # Validate and parse the refresh token
            refresh = RefreshToken(refresh_token)
            
            return Response({
                'accessToken': str(refresh.access_token),
                'msg': 'Access token refreshed successfully'
            }, status=status.HTTP_200_OK)
        
        except TokenError as e:
            return Response({"error": "Invalid token or token has been blacklisted."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
