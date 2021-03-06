from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from phonenumbers import is_valid_number, parse as phonenumbers_parse
from accounts.models import User


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'passcode')


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone')


class SignInRequestSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        phone = attrs.get('username')
        if is_valid_number(phonenumbers_parse(phone, None)):
            try:
                user = User.objects.get(phone__exact=phone)
            except User.DoesNotExist:
                attrs['phone'] = phone
            else:
                if user.is_active:
                    attrs['user'] = user
                else:
                    msg = 'User is deactivate.'
                    raise exceptions.ValidationError(msg)
        else:
            msg = 'You have to provide phone number in international format.'
            raise exceptions.ValidationError(msg)
        return attrs


class SignInVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    passcode = serializers.CharField()

    def validate(self, attrs):
        helper = {
            "phone": "Phone is required",
            "passcode": "Passcode is required"
        }
        for key, value in helper.items():
            if not attrs.get(key, None):
                raise exceptions.ValidationError(value)

        phone = attrs.get('phone', None)
        passcode = attrs.get('passcode', None)
        if is_valid_number(phonenumbers_parse(phone, None)):
            if len(passcode) == 4 and passcode.isdecimal():
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    msg = 'User with provided phone does not exist'
                    raise exceptions.ValidationError(msg)
                else:
                    if passcode == user.passcode:
                        attrs['user'] = user
                        return attrs
                    else:
                        msg = 'Incorrect passcode.'
                        raise exceptions.ValidationError(msg)
            else:
                msg = 'Passcode must be 4-digit number '
                raise exceptions.ValidationError(msg)
        else:
            msg = 'Must provide phonenumber in international format.'
            raise exceptions.ValidationError(msg)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def validate(self, attrs):
        email = attrs.get('email', None)
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return attrs  # update user profile
        else:
            if email == self.instance.email:
                return attrs
            else:
                msg = 'This email is already used'
                raise exceptions.ValidationError(msg)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            attrs['user'] = user
            return attrs
        else:
            msg = {"email": "There is no account with this email"}
            raise exceptions.ValidationError(msg)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password == confirm_password:
            validate_password(password)
            return password
        else:
            msg = {"password": "Passwords did not match"}
            raise exceptions.ValidationError(msg)
