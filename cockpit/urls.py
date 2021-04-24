from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import AtivoList, AtivoCreate, AtivosDetail, AtivosUpdate, AtivosDelete, \
    UserList, UserDetail, UserCreate, UserDelete, \
    Transacoes, GetWallet


urlpatterns = [

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

    # TRANSACOES
    path('transacoes/', Transacoes.as_view(), name='transacoes'),

    # CARTEIRA
    path('wallet/', GetWallet.as_view(), name='wallet'),
    
]