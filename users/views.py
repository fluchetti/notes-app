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
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


class UserCreateView(APIView):
    """
    Vista para creacion de usuarios. Se define el metodo POST.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Manda a llamar al create de la clase del serializador.
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                'usuario': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    Vista para login de usuarios. Se define el metodo POST.
    """
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = AuthTokenSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            # Valida que las credenciales sean correctas.
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'id': user.id,
                    'email': user.email,
                    'nombre': user.name,
                    'apellido': user.last_name,
                    'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """
    Vista para deslogear usuarios. Se define el metodo POST.
    """
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        # Le borro el token de acceso al usuario cuando se desloguea.
        token = request.auth
        if token:
            token.delete()
            return Response({'Mensaje': 'Usuario deslogeado'}, status=status.HTTP_200_OK)
        return Response({'Mensaje': 'Inicia sesion.'}, status=status.HTTP_401_UNAUTHORIZED)


class UserListView(ListAPIView):
    """
    Vista para listado de usuarios.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class UserDetailDeleteView(RetrieveDestroyAPIView):
    """
    Vista para detalle de usuario.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def get(self, request):
        """
        Se filtra el usuario en funcion del parametro que se pasa en la url.
        """
        user = self.get_queryset().filter(id=request.user.id).first()
        if user is not None:
            return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
        return Response({'Error': 'No existe el usuario indicado'}, status=status.HTTP_404_NOT_FOUND)


class RequestPasswordResetView(APIView):
    """
    Vista para peticion de cambio de contraseña. Se define el metodo POST.
    """
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return CustomUser.objects.all()

    def post(self, request):
        """
        Peticiones POST.
        Se toma el mail de la request y luego se filtra buscando un usuario con el mail ingresado.
        Si no existe un usuario registrado con ese mail se envia un error. Caso contrario se manda mail
        para cambio de contraseña.
        """
        email = request.data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'Error': 'No se ha registrado un usuario con este mail.'}, status=status.HTTP_404_NOT_FOUND)
        token_generator = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # Enlace para cambio de contraseña.
        reset_link = f"https://famous-souffle-9aa4dd.netlify.app/change_password/{uid}/{token_generator}/"
        # Envio de mail.
        subject = 'Restablecer contraseña'
        message = f'Sigue este enlace para restablecer tu contraseña: {reset_link}'
        send_mail(subject, message, None, [email])
        return Response({'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Vista para cambiar la contraseña. Aqui se accede luego de requerir el cambio y seguir el link del mail.
    """
    permission_classes = [AllowAny,]

    def post(self, request, uidb64, token):
        """
        Se filtra existencia de usuario y validacion del token.
        Se cambia la contraseña del usuario con la informacion de la request.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Cambio de contraseña
            new_password = request.data.get('new_password')
            confirm_new_password = request.data.get('confirm_new_password')
            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Contraseña restablecida correctamente'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Las contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
