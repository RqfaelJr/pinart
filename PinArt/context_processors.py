from pessoas.models import Notificacao

def contador_notificacoes(request):
    tem_notificacao = False
    
    if request.user.is_authenticated:
        tem_notificacao = Notificacao.objects.filter(pessoa=request.user.pessoa, lida=False).exists()
    
    return {'tem_notificacao_nao_lida': tem_notificacao}