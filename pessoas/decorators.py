from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import redirect

def organizador_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 

        if not request.user.groups.filter(name='Organizador').exists():
            raise PermissionDenied 

        return view_func(request, *args, **kwargs)
    return _wrapped_view

def participante_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
            
        if not request.user.groups.filter(name='Participante').exists():
            raise PermissionDenied

        return view_func(request, *args, **kwargs)
    return _wrapped_view