# Generated by Django 2.2.1 on 2019-05-27 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0005_auto_20190520_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='institution_attached',
        ),
        migrations.AddField(
            model_name='certificate',
            name='student_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='student_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]