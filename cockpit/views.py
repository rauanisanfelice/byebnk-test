import logging

from datetime import  datetime
from django.contrib.auth.models import User

from rest_framework import mixins, generics, permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, OperandHolder
from rest_framework.schemas.openapi import AutoSchema

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Ativos, Wallet, Transacao
from .serializers import AtivosSerializer, AtivosCreateSerializer, \
    WalletSerializer, TransacaoSerializer, UserSerializer

logger = logging.getLogger(__name__)



class CustomAuthToken(ObtainAuthToken):
    """Solicita token para acesso

    Returns:
        token: Token do usuário
        email (str): E-mail do usuário
    """

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
            'email': user.email
        })

    
class AtivoList(mixins.ListModelMixin, generics.GenericAPIView):

    schema = AutoSchema(tags=["Ativos"])

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Ativos.objects.all()
    serializer_class = AtivosSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivoList {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Lista todos ativos."""
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """ Lista somente os ativos """
        return Ativos.objects.filter(status_ativo=True)


class AtivoCreate(mixins.CreateModelMixin, generics.GenericAPIView):

    schema = AutoSchema(tags=["Ativos"])

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Ativos.objects.all()
    serializer_class = AtivosCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivoCreate {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = AtivosCreateSerializer(data=request.data)
        serializer.user_inclusao = request.user.username
        serializer.status_ativo = True

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtivosDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):

    schema = AutoSchema(tags=["Ativos"])
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Ativos.objects.all()
    serializer_class = AtivosSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AtivosUpdateDelete(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    schema = AutoSchema(tags=["Ativos"])
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Ativos.objects.all()
    serializer_class = AtivosCreateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        serializer = AtivosCreateSerializer(data=request.data)
        serializer.user_alteracao = request.user.username
        serializer.data_alteracao = datetime.now()

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUES)

    def delete(self, request, *args, **kwargs):
        serializer = AtivosCreateSerializer(data=request.data)
        serializer.user_exclusao = request.user.username
        serializer.data_exclusao = datetime.now()
        serializer.status_ativo = False

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
