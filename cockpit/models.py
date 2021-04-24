from django.db import models
from django.contrib.auth.models import User



class Ativos(models.Model):

    TP_RF = "RF"
    TP_RV = "RV"
    TP_CP = "CR"

    CHO_TIPOS = [
        (TP_RF, "Renda Fixa"),
        (TP_RV, "Renda Váriavel"),
        (TP_CP, "Cripto Moeda"),
    ]

    identificador = models.BigAutoField(primary_key=True)
    nome = models.CharField(verbose_name='Denominação', max_length=100)
    modalidade = models.CharField(verbose_name="Modalida", max_length=10, choices=CHO_TIPOS)

    status_ativo = models.BooleanField(default=True)
    data_inclusao = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Data de inclusão")
    data_alteracao = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Data de alteração")
    data_exclusao = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Data de exclusão")

    user_inclusao = models.CharField(max_length=50, verbose_name="Usuário inclusão")
    user_alteracao = models.CharField(max_length=50, verbose_name="Usuário alteração", null=True)
    user_exclusao = models.CharField(max_length=50, verbose_name="Usuário exclusão", null=True)

    class Meta:
        ordering = ["data_inclusao"]
        verbose_name = 'Ativo'
        verbose_name_plural = 'Ativos'

    def __str__(self):
        return self.nome


class Wallet(models.Model):

    identificador = models.BigAutoField(primary_key=True)
    saldo_anterior = models.FloatField(verbose_name="Saldo anterior")
    saldo_atual = models.FloatField(verbose_name="Saldo atual")
    
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_alteracao = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Data de alteração")

    class Meta:
        ordering = ["data_alteracao"]
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'


class Transacao(models.Model):

    TP_APLICACAO = "aplicacao"
    TP_RESGATE = "resgate"

    CHO_ACAO = [
        (TP_APLICACAO, "Aplicação"),
        (TP_RESGATE, "Resgate"),
    ]

    identificador = models.BigAutoField(primary_key=True)
    preco_unitario = models.FloatField(verbose_name="Valor unitário")
    preco_total = models.FloatField(verbose_name="Valor total")
    quantidade = models.IntegerField(verbose_name="Valor")
    ip_address = models.GenericIPAddressField()
    acao = models.CharField(verbose_name="Ação", max_length=50, choices=CHO_ACAO, default=TP_APLICACAO)

    ativo = models.ForeignKey(Ativos, verbose_name="ID Ativo", on_delete=models.PROTECT)
    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    data_transacao = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, verbose_name="Data da trnsação")

    class Meta:
        ordering = ["data_transacao"]
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
    