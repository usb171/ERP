from ..models import *

class Buscas():

    def core_get_conta(usuario):
        try:
            return Conta.objects.get(user=usuario)
        except:
           return None