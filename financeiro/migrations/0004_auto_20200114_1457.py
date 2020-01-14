# Generated by Django 2.2.9 on 2020-01-14 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0001_initial'),
        ('servico', '0001_initial'),
        ('financeiro', '0003_auto_20200114_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='forma_pagamento',
            field=models.CharField(choices=[('1', 'DINHEIRO'), ('2', 'DEBITO'), ('3', 'CREDITO')], default='1', help_text='Escolha a forma de pagamento', max_length=2, verbose_name='Forma de Pagamento'),
        ),
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_apagar', models.CharField(default=0, max_length=8, null=True, verbose_name='Valor a pagar')),
                ('forma_pagamento', models.CharField(choices=[('1', 'DINHEIRO'), ('2', 'DEBITO'), ('3', 'CREDITO')], default=1, max_length=2, verbose_name='Forma de Pagamento')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='paciente.Paciente')),
                ('procedimentos', models.ManyToManyField(to='servico.Servico', verbose_name='procedimentos')),
            ],
        ),
    ]
