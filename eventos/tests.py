from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Evento, Local, Categoria 
from pessoas.models import Pessoa, Endereco, Inscricao


class EventoInscricaoTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123')
        
        self.endereco = Endereco.objects.create(cep='88900000', cidade='Araranguá', estado='SC', rua='Rua Teste', numero='100', bairro='Centro')

        self.pessoa = Pessoa.objects.create(
            user=self.user, 
            cpf='11122233344',
            data_nascimento='1990-01-01',
            telefone='48999999999',
            endereco=self.endereco
        )
        self.local = Local.objects.create(nome='Teatro Teste', endereco=self.endereco)
        self.categoria = Categoria.objects.create(nome='Teatro')

        self.evento = Evento.objects.create(
            titulo='Show de Teste',
            descricao='Evento apenas para teste automatizado',
            data_hora_inicio=timezone.now(),
            local=self.local,
            data_hora_fim=timezone.now() + timezone.timedelta(days=10),
            capacidade=100,
            organizador=self.pessoa,
        )
        self.evento.categorias.add(self.categoria)

    
    def test_toggle_inscricao(self):
        """
        Testa se clicar em confirmar inscreve, e clicar de novo remove.
        """
        self.client.login(username='testuser', password='123')
        url = reverse('confirmar_presenca', args=[self.evento.id])
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        existe_inscricao = Inscricao.objects.filter(pessoa=self.pessoa, evento=self.evento).exists()
        self.assertTrue(existe_inscricao, "A inscrição deveria ter sido criada após o primeiro clique.")
        self.client.post(url)

        existe_inscricao = Inscricao.objects.filter(pessoa=self.pessoa, evento=self.evento).exists()
        self.assertFalse(existe_inscricao, "A inscrição deveria ter sido deletada após o segundo clique.")
