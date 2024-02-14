from django.shortcuts import render
from rest_framework.views import APIView
from users.serializers import UserSerializer
from users.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UserRegisterView(APIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Manda a llamar al create de la clase del serializador.
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        print('Llego request para crear un usuario')
        print(request)
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print('Serializer valido')
            # Manda a llamar al create de la clase del serializador.
            user = serializer.save()
            print('Se creo el user ', user)
            token = Token.objects.get(user=user)
            return Response({
                'usuario': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        print('EN EL POST DE USERLOGINVIEW')
        print(request.data)
        serializer = AuthTokenSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            print('VALID SERIALIZER')
            user = serializer.validated_data['user']
            print('pase todo')
            print(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'id': user.id,
                    'email': user.email,
                    'nombre': user.name,
                    'apellido': user.last_name,
                    'token': token.key}, status=status.HTTP_200_OK)
        else:
            print('INVALID SERIALIZER')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        print('EN USERLOGOUTVIEW')
        print(request.auth)
        print(request.user)
        token = request.auth
        if token:
            token.delete()
            print('token borrado')
            return Response({'Mensaje': 'Usuario deslogeado'}, status=status.HTTP_200_OK)
        return Response({'Mensaje': 'Inicia sesion antes de cerrarla.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request):
        print(request.user)
        print(request.auth)
        if request.auth == None:
            return Response({'Error': 'Debes autenticarte para acceder a estos datos.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(self.queryset, status=status.HTTP_200_OK)


class UserDetailDeleteView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def get(self, request):
        print('EN EL GET DE USER DETAIL')
        print(request.user)
        print(request.auth)
        user = self.get_queryset().filter(id=request.user.id).first()
        if user is not None:
            print('User not None')
            print(user)
            return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
        return Response({'Error': 'No existe el usuario indicado'}, status=status.HTTP_404_NOT_FOUND)


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return CustomUser.objects.all()

    def post(self, request):
        email = request.data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'Error': 'No se ha registrado un usuario con este mail.'}, status=status.HTTP_404_NOT_FOUND)
        token_generator = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construye el enlace de restablecimiento de contraseña
        reset_link = f"http://tu-domino.com/reset-password/{uid}/{token_generator}/"

        # Envía el correo electrónico
        subject = 'Restablecer contraseña'
        message = f'Sigue este enlace para restablecer tu contraseña: {reset_link}'
        send_mail(subject, message, None, [email])

        return Response({'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña'}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'No se ha registrado un usuario con ese correo electrónico'}, status=status.HTTP_404_NOT_FOUND)

        token_generator = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construye el enlace de restablecimiento de contraseña
        reset_link = f"http://tu-domino.com/reset-password/{uid}/{token_generator}/"

        # Envía el correo electrónico
        subject = 'Restablecer contraseña'
        message = f'Sigue este enlace para restablecer tu contraseña: {reset_link}'
        send_mail(subject, message, None, [email])

        return Response({'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña'}, status=status.HTTP_200_OK)
