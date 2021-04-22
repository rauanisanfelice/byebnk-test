import logging

from django.contrib.auth.models import User

from rest_framework import mixins, generics, permissions, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, OperandHolder
from rest_framework.schemas.openapi import AutoSchema

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Ativos, Wallet, Transacao
from .serializers import AtivosSerializer, WalletSerializer, TransacaoSerializer, UserSerializer

logger = logging.getLogger(__name__)



class CustomAuthToken(ObtainAuthToken):

    schema = AutoSchema(tags=["Token"])
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class AtivoList(mixins.ListModelMixin, generics.GenericAPIView):
    """Lista todos ativos."""

    schema = AutoSchema(tags=["Ativos"])

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Ativos.objects.all()
    serializer_class = AtivosSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivoList {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
