from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import AtivoList, AtivoCreate, AtivosDetail, AtivosUpdate, AtivosDelete, \
    CustomAuthToken


urlpatterns = [

    path('token-auth/', CustomAuthToken.as_view()),

    # ATIVO
    path('ativos/', AtivoList.as_view()),
    path('ativos-add/', AtivoCreate.as_view()),
    path('ativos/<int:pk>/', AtivosDetail.as_view()),
    path('ativos/<int:identificador>/update/', AtivosUpdate.as_view()),
    path('ativos/<int:identificador>/delete/', AtivosDelete.as_view()),

    # CARTEIRA
    # path('wallet/', Wallet.as_view(), name='wallet'),

    # User
    # path('users/', include('rest_framework.urls')),
    # path('users/', UserList.as_view(), name='usuario-list'),
    # path('users/<int:pk>/', UserDetail.as_view(), name='usuario-detail'),
    
]