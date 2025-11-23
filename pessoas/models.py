from django.db import models
from django.contrib.auth.models import User


class Endereco(models.Model): 
    ESTADOS_BR = [
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
    ]

    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=ESTADOS_BR)
    cep = models.CharField(max_length=10)




    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'

class Pessoa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pessoa')
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

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
    
class Notificacao(models.Model):
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50)

    data_hora = models.DateTimeField(auto_now_add=True)
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='notificacoes')
    evento = models.ForeignKey('eventos.Evento', on_delete=models.CASCADE, related_name='notificacoes', null=True, blank=True)

    def __str__(self):
        return f'Notificação para {self.pessoa.user.username} - {"Lida" if self.lida else "Não lida"}'