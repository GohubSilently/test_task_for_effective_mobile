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
    class Meta:
        model = User
        fields = (*UserMixin.field,)

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