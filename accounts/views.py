from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .services import AuthService

from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    VerifyOTPSerializer,
    UserProfileSerializer,
)


class RegisterAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"] #type:ignore

        return Response(
            {
                "message": "OTP sent successfully",
                "username": user.username,
                "email": user.email
            },
            status=status.HTTP_200_OK
        )
    
class VerifyOTPAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data["username"]#type:ignore
            otp = serializer.validated_data["otp"] #type:ignore

            result = AuthService.verify_otp(
                username=username,
                otp=otp
            )

            if result["success"]:
                return Response(
                    result,
                    status=status.HTTP_200_OK
                )
            
            return Response(
                result,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = AuthService.get_profile(request.user) # rqst.user is an authenticated user object
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
