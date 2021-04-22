# Generated by Django 3.2 on 2021-04-22 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ativos',
            fields=[
                ('identificador', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100, verbose_name='Denominação')),
                ('modalidade', models.CharField(choices=[('RF', 'Renda Fixa'), ('RV', 'Renda Váriavel'), ('CR', 'Cripto Moeda')], max_length=10, verbose_name='Modalida')),
                ('status_ativo', models.BooleanField(default=True)),
                ('data_inclusao', models.DateTimeField(auto_now_add=True, verbose_name='Data de inclusão')),
                ('data_alteracao', models.DateTimeField(null=True, verbose_name='Data de alteração')),
                ('data_exclusao', models.DateTimeField(null=True, verbose_name='Data de exclusão')),
                ('user_inclusao', models.CharField(max_length=50, verbose_name='Usuário inclusão')),
                ('user_alteracao', models.CharField(max_length=50, null=True, verbose_name='Usuário alteração')),
                ('user_exclusao', models.CharField(max_length=50, null=True, verbose_name='Usuário exclusão')),
            ],
            options={
                'verbose_name': 'Ativo',
                'verbose_name_plural': 'Ativos',
                'ordering': ['data_inclusao'],
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('identificador', models.BigAutoField(primary_key=True, serialize=False)),
                ('saldo_anterior', models.FloatField(verbose_name='Saldo anterior')),
                ('saldo_atual', models.FloatField(verbose_name='Saldo atual')),
                ('data_alteracao', models.DateTimeField(null=True, verbose_name='Data de alteração')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallets',
                'ordering': ['data_alteracao'],
            },
        ),
        migrations.CreateModel(
            name='Transacao',
            fields=[
                ('identificador', models.BigAutoField(primary_key=True, serialize=False)),
                ('preco_unitario', models.FloatField(verbose_name='Valor')),
                ('quantidade', models.IntegerField(verbose_name='Valor')),
                ('ip_address', models.GenericIPAddressField()),
                ('acao', models.CharField(choices=[('aplicacao', 'Aplicação'), ('resgate', 'Resgate')], default='aplicacao', max_length=50, verbose_name='Ação')),
                ('data_transacao', models.DateTimeField(null=True, verbose_name='Data da trnsação')),
                ('ativo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cockpit.ativos')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cockpit.wallet')),
            ],
            options={
                'verbose_name': 'Transação',
                'verbose_name_plural': 'Transações',
                'ordering': ['data_transacao'],
            },
        ),
    ]
