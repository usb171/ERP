# Generated by Django 2.2.7 on 2019-11-20 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0003_auto_20191119_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='nomeCompleto',
            field=models.CharField(max_length=120, null=True, verbose_name='Nome Completo'),
        ),
    ]
