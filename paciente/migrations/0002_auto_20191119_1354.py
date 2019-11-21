# Generated by Django 2.2.7 on 2019-11-19 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paciente',
            options={'verbose_name': 'Paciente', 'verbose_name_plural': 'Pacientes'},
        ),
        migrations.AddField(
            model_name='paciente',
            name='ativo',
            field=models.BooleanField(default=True, null=True, verbose_name='Ativar Paciente ?'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='cep',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='CEP'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='email',
            field=models.CharField(blank=True, max_length=120, null=True, unique=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='paciente',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Whatsapp'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='cidade',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='estado',
            field=models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande Do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='nomeCompleto',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Nome Completo'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='redeSocial',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Rede Social'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='telefone',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Telefone'),
        ),
    ]
