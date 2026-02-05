from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Session, User
from .serializers import RegistrationSerializer, LoginSerializer, UpdateSerializer


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User.objects.filter(email=serializer.validated_data['email']))
            if user.is_active is False:
                return Response({'Ваш аккаунт удален!'}, status.HTTP_400_BAD_REQUEST)
            if Session.objects.filter(user=user).first() is None:
                session = Session.objects.create(user=user)
                return Response({'session_token': f'{session.session_token}'}, status.HTTP_200_OK)
            return Response({'message': 'Вы уже залогинины'}, status.HTTP_400_BAD_REQUEST)
        return Response('Что то не так с вашими данными!', status.HTTP_400_BAD_REQUEST)


class UpdateView(GenericAPIView):
    serializer_class = UpdateSerializer

    def put(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            return Response({'message': 'Вы не прередали сессию в заголовок!'}, status.HTTP_400_BAD_REQUEST)
        update_token = token.replace(' ', '').replace('Session', '')
        session = get_object_or_404(Session.objects.filter(session_token=update_token))
        serializer = UpdateSerializer(data=request.data, instance=session.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            return Response({'message': 'Вы не прередали сессию в заголовок!'}, status.HTTP_400_BAD_REQUEST)
        update_token = token.replace(' ', '').replace('Session', '')
        session = get_object_or_404(Session.objects.filter(session_token=update_token))
        session.delete()
        return Response({'message': 'Вы успешно разлогинились!'}, status.HTTP_200_OK)


class DeleteView(APIView):
    def delete(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            return Response({'message': 'Вы не прередали сессию в заголовок!'}, status.HTTP_400_BAD_REQUEST)
        update_token = token.replace(' ', '').replace('Session', '')
        session = get_object_or_404(Session.objects.filter(session_token=update_token))
        session.user.is_active = False
        session.user.save()
        session.delete()
        return Response({'message': 'Ваш аккаунт удален!'}, status.HTTP_204_NO_CONTENT)
