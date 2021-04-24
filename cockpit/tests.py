import logging

from django.test import TestCase
from django.test.utils import override_settings

from .models import Ativos, Wallet, Transacao, User
from .views import get_or_create_wallet, update_wallet


logger = logging.getLogger(__name__)

USER_ADIM = { 'username': 'admin', 'first_name': 'admin', 'email':'email@teste.com', 'password': 'admin', }



@override_settings(USE_TZ=False)
class UserTeste(TestCase):

    def setUp(self):
        self.user_teste = User.objects.create_user(**USER_ADIM)
        self.wallet = get_or_create_wallet(usuario=self.user_teste)

    def test_user_wallet_created(self):
        """Verifica se usuario e carteira foram criados"""

        usuario = User.objects.get(username="admin")
        carteira = Wallet.objects.get(usuario=usuario)
        self.assertEqual(usuario.username, self.user_teste.username)
        self.assertEqual(carteira.usuario.pk, self.wallet.usuario.pk)


@override_settings(USE_TZ=False)
class AtivosTestCase(TestCase):
    
    def setUp(self):
        self.user_teste = User.objects.create_user(**USER_ADIM)

        Ativos.objects.create(
            nome="BITCOIN",
            modalidade=Ativos.TP_CP,
            user_inclusao=self.user_teste,
        )
        Ativos.objects.create(
            nome="DOGECOIN",
            modalidade=Ativos.TP_CP,
            user_inclusao=self.user_teste,
        )

    def test_ativos(self):
        """Verifica se os ativos foram criados"""

        ativo_01 = Ativos.objects.get(nome="BITCOIN")
        ativo_02 = Ativos.objects.get(nome="DOGECOIN")

        self.assertEqual(ativo_01.pk, 1)
        self.assertEqual(ativo_02.pk, 2)


@override_settings(USE_TZ=False)
class TransacaoTestCase(TestCase):
    
    testes = [
        {"preco_unitaio": 10, "quantidade": 2, "acao": Transacao.TP_APLICACAO},
        {"preco_unitaio": 10, "quantidade": 1, "acao": Transacao.TP_RESGATE},
    ]

    def setUp(self):
        self.user_teste = User.objects.create_user(**USER_ADIM)
        self.wallet = get_or_create_wallet(usuario=self.user_teste)

        self.ativo = Ativos.objects.create(
            nome="BITCOIN",
            modalidade=Ativos.TP_CP,
            user_inclusao=self.user_teste,
        )

    def test_ativos(self):
        """Verifica se os ativos foram criados"""

        for teste in self.testes:
            preco_total = teste['preco_unitaio'] * teste['quantidade']
            acao = teste['acao']
            Transacao.objects.create(
                preco_unitario = teste['preco_unitaio'],
                preco_total = preco_total,
                quantidade = teste['quantidade'],
                ip_address = '127.0.0.1',
                acao = acao,
                ativo = self.ativo,
                wallet = self.wallet,
                usuario = self.user_teste,
            )
            self.wallet = update_wallet(self.wallet, acao, preco_total)
            if self.wallet is None:
                self.fail("Exception Rendering is not working. Try opening"
                            "/exception/. It should raise a TestException.")

        self.assertEqual(self.wallet.saldo_atual, 10)

