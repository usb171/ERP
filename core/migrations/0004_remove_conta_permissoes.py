# Generated by Django 2.2.7 on 2019-12-22 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_conta_permissoes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conta',
            name='permissoes',
        ),
    ]