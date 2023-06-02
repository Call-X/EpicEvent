from rest_framework import serializers
from core.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import AccessToken

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
            ]
        
        extra_kwards = {'password': {'write_only': True}}
        read_only_field = ['date_joined']

    def create(self, validated_data):
        user = CustomUser.objects.create(
        email=validated_data['email'],
        username=validated_data['username'],
        password = make_password(validated_data['password'])
    )
        user.set_password(validated_data['password'])
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        access = self.get_token(self.user)
        data['access'] = str(access)
        return data