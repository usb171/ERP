# Generated by Django 2.2.7 on 2020-01-10 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servico', '0001_initial'),
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agenda',
            old_name='conta',
            new_name='profissional',
        ),
        migrations.RemoveField(
            model_name='agenda',
            name='servicos',
        ),
        migrations.AddField(
            model_name='agenda',
            name='procedimentos',
            field=models.ManyToManyField(to='servico.Servico', verbose_name='procedimentos'),
        ),
    ]
