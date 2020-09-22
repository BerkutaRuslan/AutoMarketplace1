from phonenumbers import is_valid_number
from rest_framework import serializers, exceptions
from phonenumbers import is_valid_number, parse as phonenumbers_parse
from accounts.models import User


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'passcode')


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
