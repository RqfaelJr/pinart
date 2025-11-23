from django import forms
from .models import Local, Categoria, Evento, Avaliacao

class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = ['nome', 'cnpj', 'link', 'endereco']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']

class EventoForm(forms.ModelForm):

    data_hora_inicio = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )
    data_hora_fim = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.none(),
        required=True,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'descricao', 'data_hora_inicio', 'data_hora_fim', 'capacidade', 'local', 'categorias', 'imagem']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorias'].queryset = Categoria.objects.all()

    def clean(self):
        cleaned = super().clean()
        inicio = cleaned.get('data_hora_inicio')
        fim = cleaned.get('data_hora_fim')
        capacidade = cleaned.get('capacidade')

        if inicio and fim and fim <= inicio:
            raise forms.ValidationError('A data/hora de fim deve ser posterior à de início.')

        if capacidade is not None and capacidade < 0:
            self.add_error('capacidade', 'Capacidade deve ser um número não-negativo.')

        return cleaned

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']

    def clean_nota(self):
        nota = self.cleaned_data.get('nota')
        if nota is None or not (1 <= nota <= 5):
            raise forms.ValidationError('Nota deve estar entre 1 e 5.')
        return nota