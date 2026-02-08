from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User, Session, Permission, Role, Action, Resource


class UserMixin:
    field = ('first_name', 'middle_name', 'last_name',)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is  not ''}


class RegistrationSerializer(UserMixin, serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email уже существует!'
            )
        ]
    )
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (*UserMixin.field, 'email', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UpdateSerializer(UserMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = (*UserMixin.field, 'password', 'new_password')

    def validate(self, attrs):
        user = self.instance

        password = attrs.get('password')
        new_password = attrs.get('new_password')
        if new_password:
            if not password:
                raise serializers.ValidationError({'password': 'Обязателен для смены пароля!'})
            if not user.check_password(password):
                raise serializers.ValidationError({'password': 'Неверный пароль!'})
        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.pop('new_password')
        validated_data.pop('password')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance


    def to_representation(self, instance):
        result = super().to_representation(instance)
        return {key: value for key, value in result.items() if value is  not ''}

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class ChangePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    action = ActionSerializer()
    resource = ResourceSerializer()
    class Meta:
        model = Permission
        fields = '__all__'
