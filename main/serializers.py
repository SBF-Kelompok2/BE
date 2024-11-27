from rest_framework import serializers
from .models import UserData
from django.contrib.auth.models import User

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['user', 'address']

class UserSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='userdata.address', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'address']