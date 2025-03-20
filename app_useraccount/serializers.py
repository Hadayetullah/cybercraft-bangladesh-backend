from django.conf import settings
from django.utils import timezone

from django.contrib.auth import authenticate

from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
    

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # User is inactive until OTP is verified
        user.otp = get_random_string(length=6, allowed_chars='0123456789')
        user.otp_created_at = timezone.now()
        user.save()

        # Send OTP to the user's email
        send_mail(
            subject="Your OTP Code",
            message=f"Your OTP code is {user.otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return user
    



class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user.otp != data['otp']:
            raise serializers.ValidationError("Invalid OTP.")
        # if not user.otp_is_valid():
        #     raise serializers.ValidationError("OTP expired.")

        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.is_active = True  # Activate the user
        user.otp = None  # Clear the OTP after verification
        user.save()

        return user
    


class LoginSerializer(serializers.Serializer):  # Use Serializer instead of ModelSerializer
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    # def validate(self, data):
    #     email = data.get('email')
    #     password = data.get('password')

    #     if email and password:
    #         user = User.objects.get(email=email)
    #         if not user.is_active:
    #             raise serializers.ValidationError("User account is disabled.", code='user_inactive')
            
    #         user = authenticate(email=email, password=password)
    #         if user is None:
    #             raise serializers.ValidationError("Invalid email or password.", code='authentication_failed')
            
    #     else:
    #         raise serializers.ValidationError("Both email and password are required.")

    #     data['user'] = user
    #     return data

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    raise serializers.ValidationError({
                        "non_field_errors": [
                            {"message": "User account is disabled.", "code": "user_inactive"}
                        ]
                    })
                
                user = authenticate(email=email, password=password)
                if user is None:
                    raise serializers.ValidationError({
                        "non_field_errors": [
                            {"message": "Invalid email or password.", "code": "authentication_failed"}
                        ]
                    })
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "non_field_errors": [
                        {"message": "Invalid email or password.", "code": "authentication_failed"}
                    ]
                })
        else:
            raise serializers.ValidationError("Both email and password are required.")

        data['user'] = user
        return data