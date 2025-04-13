<<<<<<< HEAD
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):  #Serializador para TODAS las operaciones CRUD
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'birth_date', 'municipality',
        'locality', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},   #parametro de entrada que NUNCA SE DEVOLVERÁ
        }

    def validate_email(self, value):    #Validación en serializador (Validar datos en función el usuario, PERMISOS)
        user = self.instance # Solo tiene valor cuando se está actualizando
        # user = True siempre y cuando se esté editando (UPDATE) el modelo
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Email already in used.")
        return value
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
=======
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):  #Serializador para TODAS las operaciones CRUD
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'birth_date', 'municipality',
        'locality', 'password')
        extra_kwargs = {
            'password': {'write_only': True},   #parametro de entrada que NUNCA SE DEVOLVERÁ
        }

    def validate_email(self, value):    #Validación en serializador (Validar datos en función el usuario, PERMISOS)
        user = self.instance # Solo tiene valor cuando se está actualizando
        # user = True siempre y cuando se esté editando (UPDATE) el modelo
        if CustomUser.objects.filter(email=value).exclude(pk=user.pk if user else None).exists():
            raise serializers.ValidationError("Email already in used.")
        return value
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
>>>>>>> main
    new_password = serializers.CharField(required=True)