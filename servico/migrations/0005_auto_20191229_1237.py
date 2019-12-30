# Generated by Django 2.2.7 on 2019-12-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0004_auto_20191227_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='valor_clinica',
            field=models.CharField(default='0', help_text='Valor de lucro da clínica', max_length=6, null=True, verbose_name='Valor clínica'),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_mao_obra',
            field=models.CharField(default='0', help_text='Valor de custo do profissional para realizar o serviço', max_length=6, null=True, verbose_name='Valor da mão de obra'),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_produtos',
            field=models.CharField(default='0', help_text='Soma de cada produto', max_length=6, null=True, verbose_name='Soma dos produtos'),
        ),
        migrations.AlterField(
            model_name='servico',
            name='valor_total',
            field=models.CharField(default='0', help_text='Valor total do serviço', max_length=6, null=True, verbose_name='Valor total'),
        ),
    ]
