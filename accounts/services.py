from .models import User, OTP
from .utils import generate_otp, send_otp_email
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

class AuthService:

    @staticmethod
    def register_user(validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
    @staticmethod
    def login_user(username, password):

        user = authenticate(  #authenticate is an built in function which compare the data with database's data and hashes the password and compare it with database's password
            username=username,
            password=password
        )

        if not user:
            return None
        
        otp = generate_otp()

        OTP.objects.create(
            user=user,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=5)
        )

        send_otp_email(
            user.email,
            otp
        )

        return user
    
    @staticmethod
    def verify_otp(username, otp):

        try:
            user = User.objects.get(username=username)
        except:
            if User.DoesNotExist:
                return {
                    "success":False,
                    "message":"User does not exist."
                }
        otp_record = (
            OTP.objects.filter(user=user)
            .order_by("-created_at")
            .first()
        )

        if not otp_record:
            return{
                "success":False,
                "message":"OTP not found."
            }
        
        if otp_record.otp != otp:
            return{
                "success":False,
                "message":"Invalid OTP."
            }
        
        if timezone.now()>otp_record.expires_at:
            return{
                "success":False,
                "message":"OTP has expired."
            }
        
        if otp_record.is_used:
            return{
                "success":False,
                "message":"OTP has already been used."
            }
        
        otp_record.is_used = True
        otp_record.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return{
            "success": True,
            "message": "OTP verified successfully.",
            "access": str(access),
            "refresh": str(refresh)
        }
    
    @staticmethod
    def get_profile(user):
        return user