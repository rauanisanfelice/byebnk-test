import logging

from datetime import  datetime

from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from rest_framework import mixins, generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from .models import Ativos, Wallet, Transacao
from .serializers import AtivosSerializer, AtivosCreateSerializer, \
    WalletSerializer, TransacaoSerializer, UserSerializer

logger = logging.getLogger(__name__)



class CustomAuthToken(ObtainAuthToken):
    """Solicita token para acesso"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['Token'],)
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
    """Lista de Ativos"""

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtivosDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """Informações do Ativo"""

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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
        
