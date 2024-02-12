from rest_framework import serializers
from users.models import CustomUser
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.Serializer):
    """
    Serializador de usuarios.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # Se ejecuta luego de que se guarde una instancia del serializador.
        print('en el create de user serializer')
        email = validated_data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            print('Ya hay un user con ese email, usa otro, ', user)
            raise serializers.ValidationError(
                {'email': 'El correo electronico que ingresaste ya esta en uso.'})
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        # Tengo que crearle el token
        token = Token.objects.create(user=user)
        return user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'name': instance.name,
            'last_name': instance.last_name,
            'created': instance.created.date(),
            'modified': instance.modified.date()
        }
