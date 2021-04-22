from django.urls import path
from django.contrib.auth import views as auth_views

from .views import ProdutoList, ProdutoDetail, CategoriaList, CategoriaDetail, \
    UserList, UserDetail


urlpatterns = [

    # ATIVO
    path('ativos/', AtivoList.as_view(), name='ativo-list'),
    path('ativos/add/', AtivoCreate.as_view(), name='ativo-create'),
    path('ativos/<int:pk>/', AtivoDetail.as_view(), name='ativo-detail'),
    path('ativos/<int:pk>/remove/', AtivoRemove.as_view(), name='ativo-remove'),
    path('ativos/<int:pk>/update/', AtivoUpdate.as_view(), name='ativo-update'),

    # CARTEIRA
    path('wallet/', Wallet.as_view(), name='wallet'),

    # User
    path('users/', UserList.as_view(), name='usuario-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='usuario-detail'),
    
]