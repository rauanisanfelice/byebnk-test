import logging

from datetime import  datetime

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from rest_framework import mixins, generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from .models import Ativos, Wallet, Transacao, User
from .serializers import AtivosSerializer, AtivosCreateSerializer, \
    WalletSerializer, TransacaoSerializer, UserSerializer, UserCreateSerializer

logger = logging.getLogger(__name__)



# USUARIOS
class UserList(mixins.ListModelMixin, generics.GenericAPIView):
    """Lista todos usuários."""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"UserList {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuários'])
    def get(self, request, *args, **kwargs):
        """Lista todos ativos."""
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """ Lista somente os ativos """
        return User.objects.filter(is_active=True)


class UserDetail(generics.RetrieveAPIView):
    """Informações do usuário."""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"UserDetail {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuários'],)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserCreate(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Adiciona um novo Usuário"""

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"UserCreate {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuários'],)
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.create_user(
                    username=serializer.data['username'],
                    password=serializer.data['password'],
                    first_name=serializer.data['first_name'],
                    last_name=serializer.data['last_name'],
                    email=serializer.data['email'],
                )
                
                Wallet.objects.create(
                    saldo_anterior=0,
                    saldo_atual=0,
                    data_alteracao=datetime.now(),
                    usuario=user,
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except Exception as error:
                logger.error(f'Erro - {erro}')
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(mixins.DestroyModelMixin, generics.GenericAPIView):
    """Remove Usuário"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"UserDelete {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Usuários'])
    def delete(self, request, *args, **kwargs):

        user = User.objects.get(pk=kwargs['pk'])
        user.is_active = False
        user.save()

        return Response(model_to_dict(user), status=status.HTTP_204_NO_CONTENT)
        

# ATIVOS
class AtivoList(mixins.ListModelMixin, generics.GenericAPIView):
    """Lista de Ativos"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ativos.objects.all()
    serializer_class = AtivosSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivoList {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: AtivosSerializer(many=True)},
        tags=['Ativos'], 
    )
    def get(self, request, *args, **kwargs):
        """Lista todos ativos."""
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        """ Lista somente os ativos """
        return Ativos.objects.filter(status_ativo=True)


class AtivoCreate(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Adiciona um novo Ativo"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ativos.objects.all()
    serializer_class = AtivosCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivoCreate {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Ativos'],)
    def post(self, request, *args, **kwargs):
        serializer = AtivosCreateSerializer(data=request.data)
        serializer.user_inclusao = request.user.username
        serializer.status_ativo = True

        if serializer.is_valid():
            ativo = Ativos.objects.create(
                nome=serializer.data['nome'],
                modalidade=serializer.data['modalidade'],
                user_inclusao=request.user.username,
            )
            return Response(model_to_dict(ativo), status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtivosDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Informações do Ativo"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ativos.objects.all()
    serializer_class = AtivosSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivosDetail {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Ativos'],)
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AtivosUpdate(mixins.UpdateModelMixin, generics.GenericAPIView):
    """Atualiza dados de um Ativo"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ativos.objects.all()
    serializer_class = AtivosCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivosUpdate {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Ativos'])
    def put(self, request, *args, **kwargs):
        serializer = AtivosCreateSerializer(data=request.data)
        if serializer.is_valid():
            ativo = Ativos.objects.get(pk=kwargs['identificador'])
            ativo.nome = serializer.data['nome']
            ativo.modalidade = serializer.data['modalidade']
            ativo.user_alteracao = request.user.username
            ativo.data_alteracao = datetime.now()
            ativo.save()

            return Response(model_to_dict(ativo), status=status.HTTP_204_NO_CONTENT)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUES)


class AtivosDelete(mixins.DestroyModelMixin, generics.GenericAPIView):
    """Remove Ativo"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ativos.objects.all()
    serializer_class = AtivosCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"AtivosDelete {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Ativos'])
    def delete(self, request, *args, **kwargs):

        ativo = Ativos.objects.get(pk=kwargs['identificador'])
        ativo.status_ativo = False
        ativo.user_exclusao = request.user.username
        ativo.data_exclusao = datetime.now()
        ativo.save()

        return Response(model_to_dict(ativo), status=status.HTTP_204_NO_CONTENT)
        

# TRANSACOES
class Transacoes(generics.GenericAPIView):
    """Realiza transações"""

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransacaoSerializer

    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Transacoes {request.method} ({request.user.username})")
        return super().dispatch(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Transações'])
    def post(self, request, *args, **kwargs):
        try:

            serializer = TransacaoSerializer(data=request.data)
            if serializer.is_valid():
                user = User.objects.get(pk=request.user.pk)
                wallet = get_object_or_404(Wallet, usuario=user)
                ativo = get_object_or_404(Ativos, pk=serializer.data['ativo'])
                acao = serializer.data['acao']
                quantidade = serializer.data['quantidade']
                preco_unitario = serializer.data['preco_unitario']

                transacao = Transacao(
                    preco_unitario=preco_unitario,
                    quantidade=quantidade,
                    ip_address=self.request.META['REMOTE_ADDR'],
                    acao=acao,
                    ativo=ativo,
                    wallet=wallet,
                    usuario=user,
                )
                
                wallet.data_alteracao = datetime.now()
                wallet.saldo_anterior = wallet.saldo_atual
                if acao == Transacao.TP_APLICACAO:
                    wallet.saldo_atual += preco_unitario
                elif acao == Transacao.TP_RESGATE:
                    wallet.saldo_atual -= preco_unitario
                else:
                    logger.error(f'Acao não é válida {acao}')
                    return Response(status=status.HTTP_400_BAD_REQUEST)

                transacao.save()
                wallet.save()

                return Response(status=status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as erro:
            logger.error(f'Erro - {erro}')
            return Response(erro, status=status.HTTP_400_BAD_REQUEST)

