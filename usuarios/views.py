from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth,messages
from churras.models import Prato

def campo_vazio(campo):
    return not campo.strip()

def senha_nao_sao_iguais(senha,senha2):
    return senha != senha2
# Create your views here.
def cadastro(request):
    # print(f'Method: {request.method}')
    if request.method == 'POST':
        # print(f'POST: {request.POST}')
        nome=request.POST['nome']
        email=request.POST['email']
        senha=request.POST['senha']
        senha2=request.POST['senha2']

        if campo_vazio(nome):
            messages.error(request,'o campo nome não pode estar vazio')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request,'o campo email não pode estar vazio')
            return redirect('cadastro')
        if senha_nao_sao_iguais(senha,senha2) or campo_vazio(senha) or campo_vazio(senha2):
            messages.error(request,'Corrija a senha - As senhas devem ser iguais e não pode estar em branco')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Esse email ja é cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request,'Esse nome ja é cadastrado')
            return redirect('cadastro')
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request,'usuario cadastrado com sucesso')
        return redirect('login')
    

    return render(request,'cadastro.html')
def login(request):

    if request.method == 'POST':
        email=request.POST['email'].strip()
        senha=request.POST['senha'].strip()
        
        if email=="" or senha=='':
            messages.error(request,'Os campos email e senha não podem ficar em branco')
            return redirect('login')
        print(email,senha)
        if User.objects.filter(email=email).exists():
            nome=User.objects.filter(email=email).values_list('username',flat=True).get()
            user= auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request, user)
                messages.success(request,'Login realizado com sucesso')
                print('Login efetuado com sucesso')
                return redirect ('dashboard')
        
        messages.error(request,'Usuario e/ou senha incorreto')
        return redirect('login')
    
    return render(request,'login.html')
def dashboard(request):
    if request.user.is_authenticated:
        pratos= Prato.objects.filter(pessoa=request.user.id).order_by('-date_prato')
        contexto = {
        'lista_pratos' : pratos,
        }
        return render (request,'dashboard.html', contexto)
    messages.error(request,'Voce nao tem permissão para acessar o dashboard.')
    return render(request,'dashboard.html')
def logout(request):
    auth.logout(request)
    print('Voce realizou o logout')
    return redirect ('index')
def criar_prato(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            #RECUPERAR DADOS DO FORMULARIO
            nome_prato=request.POST['nome_prato']
            ingredientes=request.POST['ingredientes']
            modo_preparo=request.POST['modo_preparo']
            tempo_preparo=request.POST['tempo_preparo']
            rendimento=request.POST['rendimento']
            categoria=request.POST['categoria']
            foto_prato=request.FILES['foto_prato']
            user = get_object_or_404(User,pk=request.user.id)
            prato=Prato.objects.create(pessoa=user, nome_prato=nome_prato,ingredientes=ingredientes, modo_preparo=modo_preparo,tempo_preparo=tempo_preparo, rendimento=rendimento,categoria=categoria,foto_prato=foto_prato )
            prato.save()
            print("prato criado com sucesso")
            return redirect('dashboard')
        return render(request,'criar_prato.html')
    
    messages.error(request,'Voce nao tem permissão para criar pratos.')
    return redirect ('index')

def deleta_prato(request, prato_id):
    #print(f'\n\n Entrou em deleta_prato. Excluir {prato_id}')
    try:
        prato = get_object_or_404(Prato, pk=prato_id)
    
    except:
        messages.error(request,'Prato não existente')
        return redirect ('dashboard')
    
    prato.delete()
    messages.success(request,'Prato apagado com sucesso')
    return redirect('dashboard')

def edita_prato(request, prato_id):
    try:
        prato = get_object_or_404(Prato, pk=prato_id)
    
    except:
        messages.error(request,'Prato não existente')
        return redirect ('dashboard')
    
    contexto = {
        'prato' : prato,
        }
    return render (request,'edita_prato.html', contexto)

def atualiza_prato(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            #RECUPERAR DADOS DO FORMULARIO
            prato_id=request.POST['']
            nome_prato=request.POST['nome_prato']
            ingredientes=request.POST['ingredientes']
            modo_preparo=request.POST['modo_preparo']
            tempo_preparo=request.POST['tempo_preparo']
            rendimento=request.POST['rendimento']
            categoria=request.POST['categoria']
            foto_prato=request.FILES['foto_prato']

            prato=Prato.objects.get(pk=prato_id)

            prato.nome_prato=nome_prato
            prato.ingredientes=ingredientes
            prato.modo_preparo=modo_preparo
            prato.tempo_preparo=tempo_preparo
            prato.rendimento=rendimento
            prato.categoria=categoria
             if 'foto_prato' in request.FILES:
                prato.foto_prato=request.FILES['foto_prato'] 


            user = get_object_or_404(User,pk=request.user.id)
            prato=Prato.objects.create(pessoa=user, nome_prato=nome_prato,ingredientes=ingredientes, modo_preparo=modo_preparo,tempo_preparo=tempo_preparo, rendimento=rendimento,categoria=categoria,foto_prato=foto_prato )
            prato.save()
            print("prato criado com sucesso")
            return redirect('dashboard')
        return render(request,'criar_prato.html')
    
    messages.error(request,'Voce nao tem permissão para criar pratos.')
    return redirect ('index')
