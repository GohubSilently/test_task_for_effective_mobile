from rest_framework import serializers

from users.models import User, Session



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'email')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name')
