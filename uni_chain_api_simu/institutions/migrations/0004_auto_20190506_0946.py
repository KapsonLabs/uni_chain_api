# Generated by Django 2.2.1 on 2019-05-06 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0003_auto_20190506_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='institution_attached',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='institution_attached', to='institutions.Institution'),
        ),
        migrations.CreateModel(
            name='CertificateVerificationRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('certificate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_to_be_verified', to='institutions.Certificate')),
                ('institution_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institution_to_verify', to='institutions.Institution')),
            ],
        ),
    ]
