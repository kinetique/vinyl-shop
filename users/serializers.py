from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
import re


class UserSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_check']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8, 'max_length': 128},
            'username': {'write_only': True, 'min_length': 6, 'max_length': 30},
            'email': {'write_only': True, 'max_length': 254},
        }

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError('Invalid email')
        return value

    def validate(self, data):
        if data.get('password') != data.get('password_check'):
            raise serializers.ValidationError('Passwords do not match')

        validate_password(data['password'])
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')

        return User.objects.create_user(
            password=password,
            first_name=first_name,
            last_name=last_name,
            **validated_data
        )
