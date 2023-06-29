from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from churras.models import Prato
# Create your views here.
def cadastro(request):
    # print(f'Method: {request.method}')
    if request.method == 'POST':
        # print(f'POST: {request.POST}')
        nome=request.POST['nome']
        email=request.POST['email']
        senha=request.POST['senha']
        senha2=request.POST['senha2']

        if not nome.strip():
            print('o campo nome não pode estar vazio')
            return redirect('cadastro')
        if not email.strip():
            print('o campo email não pode estar vazio')
            return redirect('cadastro')
        if senha != senha2 or not senha.strip() or not senha2.strip():
            print('Corrija a senha - As senhas devem ser iguais e não pode estar em branco')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            print('Esse email ja é cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            print('Esse nome ja é cadastrado')
            return redirect('cadastro')
        
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        print('usuario cadastrado com sucesso')
        return redirect('login')
    
    return render(request,'cadastro.html')
def login(request):

    if request.method == 'POST':
        email=request.POST['email'].strip()
        senha=request.POST['senha'].strip()
        
        if email=="" or senha=='':
            print('Preencha os campos email e senha')
            return redirect('login')
        print(email,senha)
        if User.objects.filter(email=email).exists():
            nome=User.objects.filter(email=email).values_list('username',flat=True).get()
            user= auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request, user)
                print('Login efetuado com sucesso')
                return redirect ('dashboard')
        
        print('Usuario e/senha incorreto')
        return redirect('login')
    
    return render(request,'login.html')
    

def dashboard(request):
    if request.user.is_authenticated:
        pratos= Prato.objects.filter(publicado=True).order_by('-date_prato')
        contexto = {
        'lista_pratos' : pratos,
        }
        return render (request,'dashboard.html')
    return render(request,'dashboard.html')

def logout(request):
    auth.logout(request)
    print('Voce realizou o logout')
    return redirect ('index')


def criar_prato(request):
    ...
    return render(request,'criar_prato.html')
