from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Ativos, Wallet, Transacao


class AtivosSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ativos
        fields = '__all__'


class AtivosCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ativos
        fields = ['nome', 'modalidade']


class WalletSerializer(serializers.ModelSerializer):

    class Meta:

        model = Wallet
        fields = '__all__'


class TransacaoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Transacao
        fields = ['preco_unitario', 'quantidade', 'acao', 'ativo', 'wallet']


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = '__all__'



class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['password', 'username', 'first_name', 'last_name', 'email']
