from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True, default='')
    last_name = serializers.CharField(required=False, allow_blank=True, default='')
    email = serializers.EmailField(required=False, allow_blank=True, default='')
    phone = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'phone']

    def create(self, validated_data):
        phone = validated_data.pop('phone', '')
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''),
                email=validated_data.get('email', ''),
            )
            Profile.objects.create(user=user, phone=phone)
            return user

class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        ident = attrs.get('username', '').strip()
        if '@' in ident:
            try:
                u = User.objects.get(email__iexact=ident)
                attrs['username'] = u.username
            except User.DoesNotExist:
                pass
        return super().validate(attrs)

class MeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', read_only=True, default='')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'is_staff']