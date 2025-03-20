
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

# class RegisterView(APIView):
#     permission_classes = [AllowAny]  # Allow anyone to access this view
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             email = serializer.data.get('email')
#             return Response({'msg': 'OTP sent to your email.', 'email': email}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            email = serializer.data.get('email')
            return Response({'msg': 'OTP sent to your email.', 'email': email}, status=status.HTTP_201_CREATED)
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
