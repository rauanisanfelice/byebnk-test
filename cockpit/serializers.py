from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Ativos, Wallet, Transacao


class AtivosSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ativos
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):

    class Meta:

        model = Wallet
        fields = '__all__'


class TransacaoSerializer(serializers.ModelSerializer):

    class Meta:

        model = Transacao
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = '__all__'