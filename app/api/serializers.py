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

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance