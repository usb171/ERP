# Generated by Django 2.2.7 on 2019-12-27 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0006_auto_20191227_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='quantidade',
            field=models.CharField(default='1', max_length=4, null=True, verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='valor',
            field=models.CharField(default='0', max_length=6, null=True, verbose_name='Valor do produto'),
        ),
    ]