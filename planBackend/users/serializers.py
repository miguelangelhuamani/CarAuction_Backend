from rest_framework import serializers
from .models import CustomUser, UserWallet

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
    new_password = serializers.CharField(required=True)



"""
Serializadores asociados a la gestión de carteras
"""

class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ['card_number']
    
    def validate_card_number(self, value):
        if not value.isdigit():
            print("error")
            raise serializers.ValidationError("Error: Card number must contain digits only.")

        return value

class WalletDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = "__all__"

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)


class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount to withdraw must be positive.")
        return value