from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from todolist.core.fields import PasswordField
from todolist.core.models import User
from rest_framework.relations import HyperlinkedRelatedField


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Create user, make them type password twice.
    """
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')

    def create(self, validated_data) -> User:
        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'])
        if not user:
            raise AuthenticationFailed
        return user


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name', 'email')
#
#
# class UpdatePasswordSerializer(serializers.Serializer):
#     old_password = PasswordField(required=True)
#     new_password = PasswordField(required=True)
#
#     def validate_old_password(self, value):
#         if not self.instance.check_password(value):
#             raise ValidationError({'old_password': 'Password is incorrect.'})
#         return value
#
#     def update(self, instance: User, validated_data: dict) -> User:
#         instance.set_password(validated_data['new_password'])
#         instance.save(update_fields=('password',))
#         return instance
#
#     def create(self, validated_data):
#         raise NotImplementedError
#
#
# class TgUserConnectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TgUser
#         fields = '__all__'
#         read_only_fields = ('id', 'user')
#
#
# class TgUserRelatedField(HyperlinkedRelatedField):
#     """
#     needed to make delete possible with tg_user in request params.
#     """
#     lookup_field = 'tg_user'
#
#
# class TgUserDeleteSerializer(serializers.HyperlinkedModelSerializer):
#     serializer_related_field = TgUserRelatedField
#
#     class Meta:
#         model = TgUser
#         fields = '__all__'
#
#
# class TgUserSerializer(serializers.ModelSerializer):
#     """
#     This is a PATCH, thus it does not work with HiddenField for some reason (commented out below).
#     Have to use self.context.user
#     """
#     # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = TgUser
#         fields = '__all__'
#         read_only_fields = ('id',)  # 'user')
#
#     def update(self, instance, validated_data):
#         user = self.context['request'].user
#         instance.user = user
#         instance.save()
#         return instance
