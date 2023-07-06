from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator
from .models import Prato

def index(request):
    pratos= Prato.objects.filter(publicado=True).order_by('-date_prato')
    qtde_pratos_por_pagina=3
    paginator=Paginator(pratos,qtde_pratos_por_pagina)
    page=request.GET.get('page')
    lista_pratos_pagina=paginator.get_page(page)

    contexto = {
        'lista_pratos' : pratos,
        
    }
    return render(request, 'index.html', contexto)
    # return HttpResponse('<h1>Churrasco-canes</h1')

def churrasco(request, prato_id):
    prato = get_object_or_404(Prato, pk=prato_id)
    
    contexto = {
        'prato' : prato
    }
    return render(request, 'churrasco.html', contexto)

def buscar(request):
    pratos= Prato.objects.filter(publicado=True).order_by('-date_prato')

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        pratos = pratos.filter(nome_prato__icontains = nome_a_buscar)
    
    contexto = {
        'lista_pratos' : pratos,
        
    }    
    
    return render(request, 'buscar.html', contexto)