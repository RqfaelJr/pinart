from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Local(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    link = models.URLField()
    endereco = models.ForeignKey('pessoas.Endereco', on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    capacidade = models.IntegerField()
    local = models.ForeignKey(Local, on_delete=models.CASCADE, blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, related_name='eventos')
    organizador = models.ForeignKey('pessoas.Pessoa', on_delete=models.CASCADE, related_name='eventos_organizados', blank=True, null=True)
    imagem = models.ImageField(upload_to='capas_eventos/', blank=True, null=True)

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True, default='')
    data_hora = models.DateTimeField(auto_now_add=True)
    pessoa = models.ForeignKey('pessoas.Pessoa', on_delete=models.CASCADE, related_name='avaliacoes', null=True, blank=True)

    def __str__(self):
        return f'Avaliação {self.nota} para {self.evento.titulo}'
    

