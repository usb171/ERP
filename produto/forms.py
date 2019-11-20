from django.forms import ModelForm
from django import forms

from produto.models import Produto


class ProdutoForm(ModelForm):
    class Meta:
        model = Produto
        fields = ['nome_produto', 'valor_produto']

class CadastroProdutoForm(forms.Forms):
    nome_produto = forms.CharField(required=True)
    valor_produto = forms.CharField(required=True)

    def save(self):
        if self.is_valid():
            status = {'form': self.cleaned_data}
            produto = Produto.objetcs.create(**self.cleaned_data)
            produto.save()
            return status

    def editar(self, produto):
        if self.is_valid():
            status = {'form': self.cleaned_data}
            produto = Produto.objects.get(pk=produto.id)
            produto.nome_produto = self.cleaned_data['nome_produto']
            produto.valor_produto = self.cleaned_data['valor_produto']

            produto.save()
            return status
        else:
            status = {'form': self.cleaned_data}
            return status

    def getForm(self, produto):
        return {'form': Produto.objects.filter(pk=produto.id).values()[0]}

    def is_valid(self):
        super(CadastroProdutoForm, self).is_valid()
        return True