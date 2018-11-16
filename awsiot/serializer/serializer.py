from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_password(self, value):
        return make_password(value, salt='pbkdf2_sha256')

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError("username is exist")
