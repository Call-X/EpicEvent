from rest_framework import serializers
from core.models import CustomUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = [
            'email',
            'password',
            'date_of_birth',
            'usergroup',
            ]
        
        extra_kwards = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
        email=validated_data['email'],
        date_of_birth=validated_data['date_of_birth'],
        password = make_password(validated_data['password'])
    )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class MyTokenObtainPairSerializer(TokenObtainSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['name'] = user.name
        return token