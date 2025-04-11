from django import forms
from .models import Venda, Cliente, Produto, ItemVenda

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'forma_pagamento', 'desconto', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'desconto': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ItemVendaForm(forms.ModelForm):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control produto-select'})
    )
    
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 1
            }),
        }


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['codigo', 'nome', 'preco', 'estoque', 'estoque_minimo', 'descricao']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'codigo': 'Código do Produto',
            'preco': 'Preço (R$)',
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Produto.objects.filter(codigo=codigo).exists() and not self.instance.pk:
            raise forms.ValidationError('Este código já está em uso por outro produto.')
        return codigo