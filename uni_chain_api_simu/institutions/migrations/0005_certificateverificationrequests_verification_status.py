# Generated by Django 2.2.1 on 2019-05-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0004_auto_20190506_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificateverificationrequests',
            name='verification_status',
            field=models.BooleanField(default=False),
        ),
    ]
