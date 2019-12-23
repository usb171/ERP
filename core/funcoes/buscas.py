from ..models import *
from django.contrib.auth.models import Permission

class Buscas():

    def core_get_conta(usuario):
        try:
            conta = Conta.objects.get(user=usuario)
            # print(type(Permission.objects.all()[0]))
            return conta
        except:
           return None