from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

import datetime
from django.utils.timezone import now
import random
from django.core.mail import send_mail
from datetime import timedelta
import pytz

from django.core.mail import send_mail
import random
from django.conf import settings

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .utils import *

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    # phone = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # Save OTP to the database
        EmailOTP.objects.update_or_create(email=validated_data['email'], defaults={'otp': otp})
        email = validated_data['email']
        # Send OTP via email
        send_registration_otp_email(email, otp)

        return {'email': validated_data['email'], 'message': 'OTP sent to email'}

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get("email")

        try:
            otp_record = EmailOTP.objects.get(email=email)
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError({"email": "No OTP found. Please request a new one."})

        # Check if OTP is still valid
        expiration_time = otp_record.created_at + timedelta(minutes=5)
        if now() <= expiration_time:
            otp = otp_record.otp  # Use the existing OTP
        else:
            # Generate a new OTP
            otp = str(random.randint(100000, 999999))
            otp_record.otp = otp
            otp_record.created_at = now()
            otp_record.save()

        # Send OTP via email
        send_registration_otp_email(email, otp)

        return {"message": "OTP resent to email"}


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            otp_instance = EmailOTP.objects.get(email=data['email'])
        except EmailOTP.DoesNotExist:
            raise serializers.ValidationError("Invalid email or OTP")

        if otp_instance.otp != data['otp']:
            raise serializers.ValidationError("Incorrect OTP")

        if not otp_instance.is_valid():
            raise serializers.ValidationError("OTP has expired")

        return data

    def create(self, validated_data):
        # Create user after OTP verification
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password']
        )
        # Remove OTP entry after successful registration
        EmailOTP.objects.filter(email=validated_data['email']).delete()
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{self.context['request'].scheme}://{self.context['request'].get_host()}/reset-password-confirm/{uid}/{token}/"
        
        subject = "Password Reset Requested"
        message = f"Hi your Username is : {user.username},\n\nClick the link below to reset your password:\n{reset_link}\n\nThis link will expire in 24 hours.\n\nIf you didn’t request this, ignore this email."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        
            
class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
 






class BoxSizeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxSizeModel
        fields = '__all__'


class BoxModelSerializer(serializers.ModelSerializer):
    sizes = BoxSizeModelSerializer(many=True, read_only=True)
    paper_type = serializers.SerializerMethodField()
    
    class Meta:
        model = BoxModel
        fields = '__all__'
    
    def get_paper_type(self, obj):
        paper_types = ['BROWN', 'WHITE']
        
        return paper_types
        

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone_number', 'subject', 'message', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
