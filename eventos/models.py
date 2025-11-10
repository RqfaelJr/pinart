from django.db import models

class Local(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    link = models.URLField()
    # TODO Adicionar endereço quando o modelo de endereço estiver pronto

    def __str__(self):
        return self.nome

class Midia(models.Model):
    url = models.URLField()
    descricao = models.CharField(max_length=255, blank=True)
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='midias')

    def __str__(self):
        return self.url

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

    # Adicionar organizador quando o modelo de usuário estiver pronto

    def __str__(self):
        return self.titulo


class Avaliacao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField()
    comentario = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    # TODO adicionar participante quando o modelo de usuário estiver pronto
    def __str__(self):
        return f'Avaliação {self.nota} para {self.evento.titulo}'
    

