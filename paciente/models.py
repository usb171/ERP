from django.db import models


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.IntegerField()
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    rede_social = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

