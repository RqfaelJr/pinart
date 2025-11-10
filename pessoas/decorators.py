# app/decorators.py
from django.contrib.auth.decorators import user_passes_test

def organizador_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='Organizador').exists(),
        login_url='sem_permissao'  # TODO : criar essa view
    )(view_func)

def participante_required(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated and u.groups.filter(name='Participante').exists(),
        login_url='sem_permissao'
    )(view_func)

