from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import AtivoList, AtivoCreate, AtivosDetail, AtivosUpdate, AtivosDelete, \
    UserList, UserDetail, UserCreate, UserDelete, \
    Transacoes, CustomAuthToken


urlpatterns = [

    path('token-auth/', CustomAuthToken.as_view()),

    # USUÁRIOS
    path('usuarios/', UserList.as_view()),
    path('usuarios-add/', UserCreate.as_view()),
    path('usuarios/<int:pk>/', UserDetail.as_view()),
    path('usuarios/<int:pk>/delete/', UserDelete.as_view()),

    # ATIVO
    path('ativos/', AtivoList.as_view()),
    path('ativos-add/', AtivoCreate.as_view()),
    path('ativos/<int:pk>/', AtivosDetail.as_view()),
    path('ativos/<int:identificador>/update/', AtivosUpdate.as_view()),
    path('ativos/<int:identificador>/delete/', AtivosDelete.as_view()),

    # CARTEIRA
    path('transacoes/', Transacoes.as_view(), name='transacoes'),

    # # CARTEIRA
    # path('wallet/', Wallet.as_view(), name='wallet'),

    # User
    # path('users/', include('rest_framework.urls')),
    # path('users/', UserList.as_view(), name='usuario-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='usuario-detail'),
    
]