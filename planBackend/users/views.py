from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, UserWallet
from .serializers import UserSerializer, ChangePasswordSerializer, UserWalletSerializer, DepositSerializer, WalletDetailSerializer, WithdrawSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class UserRegisterView(generics.CreateAPIView): # view solo de CREATE, NO es un ViewSet
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all() #Conjunto de datos que se utilizará
    serializer_class = UserSerializer   

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # Estos datos son los que el cliente ha enviado
        if serializer.is_valid():
            user = serializer.save()    # se guarda el nuevo objeto CustomUser en la base de datos
            refresh = RefreshToken.for_user(user)   # se genera un refresh token para este nuevo usuario.
            return Response({
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)  # Si el usuario se ha creado correctamente, se devuelve una respuesta
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
       

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)  
        #“Quiero actualizar el usuario autenticado (request.user) con estos datos 
        # #(request.data), pero solo los campos que vengan en la petición (partial=True)”.
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():   # Aquí "creo" mi diccionario validated_data
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Incorrect current password."},
                        status=status.HTTP_400_BAD_REQUEST)
            
            try:
                validate_password(serializer.validated_data['new_password'], user)
            except ValidationError as e:
                return Response({"new_password": e.messages},status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password updated successfully."})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """Realiza el logout eliminando el RefreshToken (revocar)"""
        try:
            # Obtenemos el RefreshToken del request
            #Se esperan que esté en el header Authorization
            refresh_token = request.data.get('refresh', None)
            if not refresh_token:
                return Response({"detail": "No refresh token provided."},
                status=status.HTTP_400_BAD_REQUEST)
            
            # Revocar el RefreshToken
            token = RefreshToken(refresh_token)
            token.blacklist()   # Lo metemos a la "lista de excluidos"
            return Response({"detail": "Logout successful"},
            status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

"""
Serializadores asociados a Wallet
"""



class WalletCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserWalletSerializer

    def perform_create(self, serializer):
        user = self.request.user
        

        if UserWallet.objects.filter(user=user).exists():
            raise ValidationError("User already has a wallet.")
        serializer.save(user=user)

class WalletDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletDetailSerializer

    
    def get_object(self):
        try:
            return UserWallet.objects.get(user=self.request.user)
        
        except UserWallet.DoesNotExist:
            raise ValidationError("User does not have a wallet yet.")


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():

            try:
                user_wallet = UserWallet.objects.get(user=request.user)
            except UserWallet.DoesNotExist:
                return Response({"detail": "No wallet found."}, status=status.HTTP_404_NOT_FOUND)

            user_wallet.balance += serializer.validated_data['amount']
            user_wallet.save()
            return Response({"detail": "Deposit successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithDrawView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user_wallet = UserWallet.objects.get(user=request.user)
            except UserWallet.DoesNotExist:
                return Response({"detail": "No wallet found."}, status=status.HTTP_404_NOT_FOUND)

            amount = serializer.validated_data['amount']

            if user_wallet.balance < amount:
                return Response({"detail": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

            user_wallet.balance -= amount
            user_wallet.save()
            return Response({"detail": "Deposit successful."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)