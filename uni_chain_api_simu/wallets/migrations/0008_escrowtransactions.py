# Generated by Django 2.2.1 on 2019-05-14 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0007_auto_20190514_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='EscrowTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('transaction_type', models.CharField(choices=[('TOP-UP', 'TOP-UP'), ('VERIFICATION', 'VERIFICATION'), ('VIEWING', 'VIEWING')], max_length=20)),
                ('amount_initiated', models.DecimalField(decimal_places=3, default=0, max_digits=20)),
                ('date_initiated', models.DateTimeField(auto_now_add=True)),
                ('date_transferred', models.DateTimeField(blank=True, null=True)),
                ('input_wallet_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escrow_input_wallet_address', to='wallets.Wallet')),
                ('output_wallet_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='escrow_output_wallet_address', to='wallets.Wallet')),
            ],
        ),
    ]
