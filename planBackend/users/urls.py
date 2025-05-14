from django.urls import path
from .views import (UserRegisterView, UserListView, UserRetrieveUpdateDestroyView, LogoutView, 
                    UserProfileView, ChangePasswordView, WalletCreate, WalletDetail,
                    WithDrawView, DepositView)

app_name="users"

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('log-out/', LogoutView.as_view(), name='log-out'),
    
    # URLs para wallet
    path('create-wallet/', WalletCreate.as_view(), name ="create-wallet"),
    path('my-wallet/', WalletDetail.as_view(), name ="my-wallet"),
    path('deposit/', DepositView.as_view(), name = "deposit"),
    path("withdraw/", WithDrawView.as_view(), name = "withdraw")
]