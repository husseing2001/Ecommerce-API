

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=40)
    last_name = serializers.CharField(max_length=40)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=65, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email exists'})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

