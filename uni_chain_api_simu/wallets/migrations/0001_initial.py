# Generated by Django 2.2.1 on 2019-05-27 09:33

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
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_number', models.CharField(blank=True, max_length=100, null=True)),
                ('wallet_address', models.CharField(blank=True, max_length=255, null=True)),
                ('wallet_private_key', models.CharField(blank=True, max_length=255, null=True)),
                ('wallet_public_key', models.CharField(blank=True, max_length=255, null=True)),
                ('wallet_balance', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('is_institution_wallet', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('wallet_owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WalletTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('transaction_type', models.CharField(choices=[('TOP-UP', 'TOP-UP'), ('VERIFICATION', 'VERIFICATION'), ('VIEWING', 'VIEWING')], max_length=20)),
                ('transaction_amount', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('date_transacted', models.DateTimeField(auto_now_add=True)),
                ('input_wallet_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='input_wallet_address', to='wallets.Wallet')),
                ('output_wallet_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='output_wallet_address', to='wallets.Wallet')),
            ],
        ),
        migrations.CreateModel(
            name='PayTokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_issued', models.CharField(max_length=400)),
                ('expected_token_cost', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('transaction_id_generated', models.CharField(blank=True, max_length=255, null=True)),
                ('token_active', models.BooleanField(default=True)),
                ('date_to_expire', models.DateTimeField(blank=True, null=True)),
                ('date_issued', models.DateTimeField(auto_now_add=True)),
                ('issued_to_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_issued_wallet_address', to='wallets.Wallet')),
                ('issuer_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_issuer_wallet_address', to='wallets.Wallet')),
            ],
        ),
        migrations.CreateModel(
            name='EscrowTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('transaction_type', models.CharField(choices=[('TOP-UP', 'TOP-UP'), ('VERIFICATION', 'VERIFICATION'), ('VIEWING', 'VIEWING')], max_length=20)),
                ('amount_initiated', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('is_document_verification', models.BooleanField(default=False)),
                ('is_certificate_view', models.BooleanField(default=False)),
                ('escrow_active', models.BooleanField(default=True)),
                ('date_initiated', models.DateTimeField(auto_now_add=True)),
                ('date_transferred', models.DateTimeField(blank=True, null=True)),
                ('input_wallet_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escrow_input_wallet_address', to='wallets.Wallet')),
                ('output_wallet_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escrow_output_wallet_address', to='wallets.Wallet')),
            ],
        ),
    ]
