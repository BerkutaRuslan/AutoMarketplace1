from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.conf import settings

from Auto_marketplace.utils import send_email
from accounts.models import ResetKey
from accounts.serializers import UserPhoneSerializer, SignInRequestSerializer, UserFullSerializer, \
    SignInVerifySerializer, UserUpdateSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from accounts.utils import send_sms_code


class SignInRequestView(APIView):
    """
      Sign In first step - phone verification
    """
    permission_classes = (AllowAny,)
    serializer_class = SignInRequestSerializer

    @swagger_auto_schema(
        operation_id="Sign In Request",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username as user\'s phone')
            },
        ),
        responses={
            200: UserPhoneSerializer,
            201: UserPhoneSerializer,
            400: "Invalid phone number"
        },
        security=[],
        tags=['accounts'],
    )
    def post(self, request):
        request_time = timezone.now()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.validated_data['user']
            except KeyError:
                user = serializer.save()

            if user.passcode_timer:
                if request_time < user.passcode_timer:
                    wait_for = (user.passcode_timer - request_time)
                    return Response({"error": f"Wait {wait_for} seconds and try again"})
            # if user is new or passcode timer has passed
            code = send_sms_code(user.phone)
            if code:
                user.passcode = code
                user.passcode_timer = timezone.now() + timezone.timedelta(minutes=1)
                user.save()

                user_serializer = UserPhoneSerializer(user)
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "message was not delivered to user"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SignInVerifyView(APIView):
    """
    Sign In second step - code verification
    """
    permission_classes = (AllowAny,)
    serializer_class = SignInVerifySerializer

    @swagger_auto_schema(
        operation_id="Sign In Verify",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['phone', 'passcode'],
            properties={
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='user\'s  phone in international format'),
                'passcode': openapi.Schema(type=openapi.TYPE_STRING, description='code from SMS'),
            },
        ),
        responses={
            200: UserPhoneSerializer,
            201: UserPhoneSerializer,
            400: "Incorrect passcode or invalid phone number"
        },
        security=[],
        tags=['accounts'],
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user.first_name != "":
                is_new_user = False
                user_serializer = UserFullSerializer(user)
            else:
                is_new_user = True
                user_serializer = UserFullSerializer(user)

            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'is_new_user': is_new_user, 'user': user_serializer.data},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileSetupView(APIView):
    """
    An endpoint for updating email, first name and last name
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    @swagger_auto_schema(
        operation_id="Setup Profile",
        operation_description="Save Profile info after successful Sign In",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'full_name'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        tags=['accounts'],
    )
    def put(self, request):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserFullSerializer(user)
            return Response({'user': user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    An endpoint for retrieving or updating User
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserFullSerializer

    @swagger_auto_schema(
        operation_id="Get User's Profile",
        operation_description="Retrieve User's Profile",
        security=[],
        tags=['accounts'],
        responses={
            200: UserFullSerializer,
            400: "Invalid token"
        },
    )
    def get(self, request):
        user = request.user
        data = self.serializer_class(user).data
        return Response({'user': data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_id='Update Profile',
        operation_description="Update Profile info (first name, last name or email)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: UserFullSerializer,
            400: "Invalid user info or token"
        },
        security=[],
        tags=['accounts'],
    )
    def put(self, request):
        serializer = UserUpdateSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserFullSerializer(user)
            return Response({'user': user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            # create reset key instance
            reset_key = ResetKey.objects.create(user=user)
            reset_key.save()

            reset_password_url = f'{settings.HOST}/accounts/reset-password?key={reset_key.reset_key}'
            send_email(subject="Reset Password", user=user.email, template='reset-password.html',
                       from_email='berkutruslan3@gmail.com',
                       content={'user_name': f"{user.first_name} {user.last_name}", 'reset_url': reset_password_url})
            return Response({'message': 'Reset link was sent successfully, check your mail box',
                             'reset_key': reset_key.reset_key}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def put(self, request):
        reset_key = request.query_params['key']
        reset_key_obj = get_object_or_404(ResetKey, reset_key=reset_key)
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = reset_key_obj.user
            user.set_password(serializer.validated_data)
            user.save()

            # delete ResetKey instance
            reset_key_obj.delete()
            return Response({'message': 'Your password has been reset'}, status=status.HTTP_200_OK)
