from statistics import mode

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import Session, User, Permission
from .permissions import CustomPermission
from .serializers import ChangePermissionSerializer, RegistrationSerializer, LoginSerializer, UpdateSerializer


@extend_schema(tags=['AUTH'])
class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = []

@extend_schema(tags=['AUTH'])
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'message': 'Пользователь с данным email не найден!'}, status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response({'message': 'Неверный пароль!'}, status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'message': 'Ваш аккаунт удален!'}, status.HTTP_400_BAD_REQUEST)
        session = Session.objects.filter(user=user).first()
        if not session:
            session = Session.objects.create(user=user)
        return Response({'session_token': f'{session.session_token}'}, status.HTTP_200_OK)

@extend_schema(tags=['PROFILE'])
class UpdateView(CustomPermission, GenericAPIView):
    serializer_class = UpdateSerializer
    resource = 'profile'

    def put(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@extend_schema(tags=['AUTH'])
class LogoutView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Вы успешно разлогинились!'}, status.HTTP_200_OK)

@extend_schema(tags=['PROFILE'])
class DeleteView(CustomPermission, APIView):
    resource = 'profile'
    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        request.auth.delete()
        return Response({'message': 'Ваш аккаунт удален!'}, status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['CHANGE_PERMISSIONS'])
class ChangePermissionViewSet(CustomPermission, ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = ChangePermissionSerializer
    resource = 'change_permissions'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check(request)


