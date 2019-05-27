# Generated by Django 2.2.1 on 2019-05-20 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0003_auto_20190516_0959'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='document_signature_link',
        ),
        migrations.AddField(
            model_name='documents',
            name='document_hash',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='certificateviewrequests',
            name='document_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='certificate_to_be_verified', to='certificates.Documents'),
        ),
    ]