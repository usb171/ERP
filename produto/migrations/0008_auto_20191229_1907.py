# Generated by Django 2.2.7 on 2019-12-29 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0007_auto_20191227_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='valor',
            field=models.CharField(default='0', max_length=8, null=True, verbose_name='Valor do produto'),
        ),
    ]
