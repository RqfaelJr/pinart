from django.db import models
from django.contrib.auth.models import User


class Endereco(models.Model): 
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'

class Pessoa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoa')
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()
    
    @property
    def tipo(self):
        grupos = self.user.groups.values_list('name', flat=True)
        if 'Organizador' in grupos:
            return 'Organizador'
        return 'Participante'

class Inscricao(models.Model): # TODO: implementar lógica de inscrição
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='inscricoes')
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    participou = models.BooleanField(default=False)

    class Meta:
        unique_together = ('pessoa', 'evento')

    def __str__(self):
        return f'Inscrição de {self.pessoa.user.username} no evento {self.evento.titulo}'